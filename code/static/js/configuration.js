
// Get the Sidebar


var alcohol_probability,cocain_probability,probability,marijuana_probability;



document.getElementById("stateContainer").style.display="none";
document.getElementById("back").style.display="none";
document.getElementById("userInputPrediction").style.display="none";

// document.getElementById("tabNavigation").style.display="none";
// document.getElementById("description").style.display="none";



 var elems = document.querySelectorAll("highcharts-credits");
    var index = 0, length = elems.length;
    for ( ; index < length; index++) {
        elems[index].style.display="none";
    }


var mySidebar = document.getElementById("mySidebar");
var myMainContainer = document.getElementById("myMainContainer");
var reSize=true;

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
        overlayBg.style.display = "none";
    } else {
        mySidebar.style.display = 'block';
        overlayBg.style.display = "block";
    }
}

// Close the sidebar with the close button
function w3_close() {
    mySidebar.style.display = "none";
    overlayBg.style.display = "none";
}



function extendSidePane(){


   var e = document.getElementById("age");
   var age = e.options[e.selectedIndex].value;

   e = document.getElementById("sex");
   var sex = e.options[e.selectedIndex].value;

   e = document.getElementById("race");
   var race = e.options[e.selectedIndex].value;

   e = document.getElementById("state");
   var state = e.options[e.selectedIndex].value;




      var data = {
        age : age,
        sex : sex,
        race : race,
        state :  state
      }

    $.ajax({
            url: '/Result',
            data: data,
            type: 'POST',
            success: function(response) {

                alcohol_probability= response.data.probability;
                var raw_probability = alcohol_probability
var probability_percentage = raw_probability * 100
var rounded = +(Math.round(probability_percentage + "e+2")  + "e-2")

                document.getElementById("alcohol_probability").setAttribute("data-percent", response.data.alcohol_probability + "%");
                document.getElementById("marijuana_probability").setAttribute("data-percent", response.data.marijuana_probability + "%");
                document.getElementById("cocain_probability").setAttribute("data-percent", response.data.cocain_probability + "%");




                // $('#elementId').append("<div id= 'alcohol_probability' class='skillbar clearfix' data-percent='"+response.data.alcohol_probability+"%'> <div class='skillbar-title' style='background: #2980b9;'><span>Alcohol</span></div> <div class='skillbar-bar' style='background: #3498db;'></div> </div>");

              jQuery('.skillbar').each(function(){
                     jQuery(this).find('.skillbar-bar').animate({
                        width:jQuery(this).attr('data-percent')
                    },2000);
                });
                document.getElementById("container-speed").innerHTML = rounded + "%";

               //chartTest( alcohol_probability);

  displayUserRelatedStateData(age,sex,race,state);
            },
            error: function(error) {
                console.log(error);
            }
     });





   document.getElementById("back").style.display="block";
   document.getElementById("submit").style.display="none";
   document.getElementById("userInputPrediction").style.display="block";
   document.getElementById("individualSubstancePrediction").style.display="none";
   mySidebar.style.width="60%";
   myMainContainer.style.width="40%";
   myMainContainer.style.transition = "width 1s";
   mySidebar.style.transition = "width 1s";
   myMainContainer.style.cssFloat = "right";
   setTimeout(function(){ resizeChart(1); }, 1000);


}




function displayUserRelatedStateData(age,sex,race,state){

    pushToSide(state);


}




function pushToSide(val){

  	document.getElementById("countryContainer").style.display = "none";
 	document.getElementById("stateContainer").style.display="block";
 	document.getElementById("stateContainer").style.backgroundColor = "white";
    document.getElementById("description").innerHTML=val + " State Drug Analytics"

  	// document.getElementById("tabNavigation").style.display="block";
  	// document.getElementById("description").style.display="block";


     $.ajax({
        type: "GET",
        url: '/stateData?state='+val,
      success: function(response){
        console.log(response);


        sex(response.state_stats.sex);
          race(response.state_stats.race);
          age(response.state_stats.age);


      }
      });


  	document.getElementById("initialTab").click(event,'Age');
  	resizeChart(1);




}

function resizeChart(check){

    height = chart.height;
    // width = $("#myMainContainer").width() ;

    if( document.getElementById("countryContainer").style.display==="none"){
    	width = $("#tabNavigation").width() ;
    	chartAge.setSize(width, height, doAnimation = true);
    	chartRace.setSize(width, height, doAnimation = true);
    	chartSex.setSize(width, height, doAnimation = true);

    }

    else {

    	width = $("#countryContainer").width() ;
      chart.setSize(width, height, doAnimation = true);
    }



}

function hideStateGraph(){

   document.getElementById("stateContainer").style.display="none";
   document.getElementById("countryContainer").style.width="100%";
   // document.getElementById("countryContainer").style.height="500px";
   document.getElementById("countryContainer").style.cssFloat = "right";
   document.getElementById("countryContainer").style.transition = "all 1s";
   setTimeout(function(){ resizeChart(0); }, 500);

}


function displayActiveGraph(element){
	element.classList.add("active");
}



function openGraph(evt, feature) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(feature).style.display = "block";
    evt.currentTarget.className += " active";


}

function backToUSMap() {

 document.getElementById("countryContainer").style.display = "block";

 document.getElementById("stateContainer").style.display="none";
 resizeChart(1);
}



function backToOriginalShape(){


   document.getElementById("userInputPrediction").style.display="none";
   document.getElementById("individualSubstancePrediction").style.display="block";
   document.getElementById("back").style.display="none";
   document.getElementById("submit").style.display="block";
   document.getElementById("individualSubstancePrediction").style.display="block";
  
   mySidebar.style.width="30%";
   myMainContainer.style.width="70%";
   myMainContainer.style.transition = "width 1s";
   mySidebar.style.transition = "width 1s";
   // myMainContainer.style.cssFloat = "right";
   setTimeout(function(){ resizeChart(1); }, 1000);

}



$.fn.redraw = function(){
  $(this).each(function(){
    var redraw = this.offsetHeight;
  });
};