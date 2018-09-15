from stk import runner

import microsoft_face
import creditsuisse
import logging

from threading import Lock
import qi
import time
import sys
#import argparse
import Image
import math
import almath

PEPPER_IP = "127.0.0.1"
PEPPER_PORT = 9559
CONNECTION_URL = "tcp://" + PEPPER_IP + ":" + str(PEPPER_PORT)

class PepUpBank(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(PepUpBank, self).__init__()
        app.start()
        self.session = app.session
        # Get the service ALMemory.
        self.memory = self.session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = self.session.service("ALTextToSpeech")
        self.leds = self.session.service("ALLeds")
        self.video_service = self.session.service("ALVideoDevice")
        self.got_face = False
        self.counter = 0
        self.creditsuisse = creditsuisse.credit_suisse()
        microsoft_face.init()
        self.mutex = Lock()

        logging.basicConfig(format="%(asctime)s [%(threadName)-10s] %(levelname)-6s %(message)s")
        self.logger = logging.getLogger("PepUpBank")
        self.logger.setLevel(logging.DEBUG)
        # self.logger.addHandler(logging.StreamHandler())

        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.subscribe("PepUpBank")

    # def reach_customer(self):
    #     return
    #
    # def handle_customer(self):
    #     return

    def on_human_tracked(self, value):
        #print("on_human_tracked(%s)" % (value))

        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            if self.mutex.acquire(False) == False:
                return
            # get face image
            """
            First get an image, then show it on the screen with PIL.
            """
            # Get the service ALVideoDevice.

            resolution = 2    # VGA
            colorSpace = 11   # RGB

            videoClient = self.video_service.subscribe("python_client", resolution, colorSpace, 5)

            t0 = time.time()

            # Get a camera image.
            # image[6] contains the image data passed as an array of ASCII chars.
            naoImage = self.video_service.getImageRemote(videoClient)

            t1 = time.time()

            # Time the image transfer.

            self.video_service.unsubscribe(videoClient)

            ledname = 'ChestLeds'
            self.leds.on(ledname)
            self.leds.fadeRGB(ledname, 1.0, 0.0, 0.0, 0);

            # Now we work with the image returned and save it as a PNG  using ImageDraw
            # package.

            # Get the image size and pixel array.
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            image_string = str(bytearray(array))

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

            imageName = "/data/home/nao/.local/share/PackageManager/apps/peppedupbank/imgs/image#"+ str(self.counter) +".png"
            self.counter += 1

            # Save the image.
            im.save(imageName, "PNG")

            self.tts.say("Hi!")
            self.logger.info("Trying to identify person ...")
            customerId = microsoft_face.most_likely_person(microsoft_face.identify_person(imageName))
            if customerId == None:
                self.logger.info("No person identified.")
                self.tts.say("I never saw you before! Nice to meet you!")
            else:
                customerId = int(customerId)
                self.logger.info("Found customer %s" % (customerId))

                userData = self.creditsuisse.get_user_data(customerId)

                for obj in userData['object']:
                    self.tts.say("You must be %s %s!" % (obj['surname'], obj['lastname']))

                    break

            self.leds.off(ledname)
            self.mutex.release()

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting PepUpBank"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping PepUpBank"
            self.face_detection.unsubscribe("PepUpBank")
            #stop
            sys.exit(0)

if __name__ == "__main__":
    try:
        # Initialize qi framework.
        app = qi.Application(["PepUpBank", "--qi-url=" + CONNECTION_URL])
    except:
        print ("Can't connect to Naoqi at ip \"" + PEPPER_IP + "\" on port " + str(PEPPER_PORT) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    pep_up_bank = PepUpBank(app)
    pep_up_bank.run()
