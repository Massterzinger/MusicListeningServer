var Auds;
var PlayingNow;

function Load(){
    Auds = document.getElementById("list").getElementsByTagName("audio");
    for(var i =0; i < Auds.length; i++){
        Auds[i].onplay = function (){
            for(var i =0; i < Auds.length; i++){
                if(Auds[i] != this){
                    Auds[i].pause();
                }
            }
        }
        Auds[i].onended = function(){
            for(var i = 0; i < Auds.length; i++){
                if(Auds[i]==this){
                    if(i == Auds.length-1)
                        Auds[0].play();
                    else
                        Auds[i+1].play();
                }
            }
        }
    }
}




