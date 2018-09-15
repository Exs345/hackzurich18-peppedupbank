from stk import runner

import microsoft_face
import creditsuisse

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
        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.subscribe("PepUpBank")
        self.got_face = False

        self.lastTime = time.time()
        self.counter = 0
        self.creditsuisse = credit_suisse()

        microsoft_face.init()

    # def reach_customer(self):
    #     return
    #
    # def handle_customer(self):
    #     return

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif time.time() > self.lastTime+5 and not self.got_face:  # only speak the first time a face appears
            self.got_face = True

            # get face image
            """
            First get an image, then show it on the screen with PIL.
            """
            # Get the service ALVideoDevice.

            video_service = self.session.service("ALVideoDevice")
            resolution = 2    # VGA
            colorSpace = 11   # RGB

            videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

            t0 = time.time()

            # Get a camera image.
            # image[6] contains the image data passed as an array of ASCII chars.
            naoImage = video_service.getImageRemote(videoClient)

            t1 = time.time()

            # Time the image transfer.
            print "acquisition delay ", t1 - t0

            video_service.unsubscribe(videoClient)

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

            print("Trying to identify person ...")
            customerId = int(microsoft_face.identify_person(imageName))
            if customerId == None:
                print("No person identified.")
            else
                print("Found customer %s" % (customerId))

                self.creditsuisse.get_user_data(customerId)

                for obj in res['object']:
                    print(obj)

                    self.tts.say("Hello %u %u!" % (obj['surname'], obj['lastname']))

                    break

            # get customer position



            # reach_customer()
            # handle_customer() # which adds face to visited (start ignoring this face)

            # print "I saw a face!"
            # self.tts.say("Hello, you!")
            # # First Field = TimeStamp.
            # timeStamp = value[0]
            # print "TimeStamp is: " + str(timeStamp)
            #
            # # Second Field = array of face_Info's.
            # faceInfoArray = value[1]
            # for j in range( len(faceInfoArray)-1 ):
            #     faceInfo = faceInfoArray[j]
            #
            #     # First Field = Shape info.
            #     faceShapeInfo = faceInfo[0]
            #
            #     # Second Field = Extra info (empty for now).
            #     faceExtraInfo = faceInfo[1]
            #
            #     print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
            #     print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
            #     print "Face Extra Infos :" + str(faceExtraInfo)

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
