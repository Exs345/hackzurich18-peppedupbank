var application = function(){
    var ALMemory = null;

    var log = function(l){
        if(console) console.log(l)  ;
    };

    function CustomerData(customer){

          var d = new Date();
          var hours = d.getHours();
          var greeting = "Good morning";
          if (hours > 17) {
            greeting = "Good evening";
          } else if (hours > 12) {
            greeting = "Good afternoon";
          }

          greeting += ", <br/>" + customer[0] + " " + customer[1];
          $("#greeting").html(greeting);
    }

	/*QiSession Events*/

    var onConnected = function(session){
        log("connected");
        session.service("ALMemory").then(function (serv) {
            ALMemory = serv;
        },
        function(error){
            log("Unable to get the service ALMemory : " + error);
        });
        RobotUtils.subscribeToALMemoryEvent("CustomerData", CustomerData);
    };

    var onError = function(){
        log("Disconnected, or failed to connect :-(");
    };

    var init = function(){
        RobotUtils.connect(onConnected, onError); // async !
        return this;
    };

    return init();
};
