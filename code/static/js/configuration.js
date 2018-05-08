
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
   avatar_img = document.getElementById("avatar")
   var topType = "ShortHairShortFlat"
   var accessoriesType = "Default"
   var hairColor = "BrownDark"
   var facialHairType = "Blank"
   var facialHairColor = "BrownDark"
   var clotheType = "BlazerShirt"
   var eyebrowType = "Default"
   var mouthType = "Smile"
   var skinColor = "Light"
    if(sex == "male") {
       if(age >= 12 && age <= 18){
           topType = "ShortHairDreads02"
           accessoriesType = "Kurt"
           clotheType = "GraphicShirt"
       }
       else if(age >= 19 && age <= 24){
           topType = "ShortHairShortFlat"
           accessoriesType = "Prescription02"
           facialHairType = "BeardLight"
           clotheType = "BlazerShirt"
           if (state == "TEXAS") {
               facialHairType = "MoustacheFancy"
               topType = "Hat"
           }
       }
       else if(age == "25_29"){
           topType = "ShortHairShortFlat"
           accessoriesType = "Prescription02"
           facialHairType = "BeardLight"
           clotheType = "BlazerShirt"
           if (state == "TEXAS") {
               facialHairType = "MoustacheFancy"
               topType = "Hat"
           }
       }
       else if(age == "30_34" || age == "35_39"){
           topType = "ShortHairShortWaved"
           accessoriesType = "Prescription01"
           clotheType = "BlazerSweater"
           facialHairType = "BeardMedium"
           facialHairColor = "Auburn"
           hairColor = "Auburn"
           if (race == "Black_sAfrican") {
               facialHairColor = "Black"
               hairColor = "Black"
            }

       }
       else if(age == "40_44" || age == "45_49" || age == "50_54"){
           topType = "ShortHairSides"
           accessoriesType = "Prescription02"
           facialHairType = "BeardMedium"
           facialHairColor = "Auburn"
           hairColor = "Auburn"
           clotheType = "CollarSweater"
           if (race == "Black_sAfrican") {
               facialHairColor = "Black"
               hairColor = "Black"
            }
       }
       else if(age == "55+"){
           topType = "ShortHairSides"
           accessoriesType = "Round"
           facialHairType = "BeardMedium"
           facialHairColor = "Platinum"
           hairColor = "SilverGray"
           clotheType = "ShirtCrewNeck"
       }
    }

    if(sex == "female") {
       if(age >= 12 && age <= 18){
           topType = "LongHairCurvy"
           accessoriesType = "Kurt"
           clotheType = "GraphicShirt"
       }
       else if(age >= 19 && age <= 24){
           topType = "LongHairFroBand"
           accessoriesType = "Prescription02"
           clotheType = "Overall"
           if (state == "FLORIDA") {
               topType = "LongHairFrida"
               clotheType = "GraphicShirt"
           }
       }
       else if(age == "25_29"){
           topType = "LongHairFroBand"
           accessoriesType = "Prescription02"
           clotheType = "Overall"
           if (state == "FLORIDA") {
               topType = "LongHairFrida"
               clotheType = "GraphicShirt"
           }
       }
       else if(age == "30_34" || age == "35_39"){
           topType = "LongHairStraightStrand"
           accessoriesType = "Prescription02"
           clotheType = "BlazerShirt"
           hairColor = "BrownDark"

       }
       else if(age == "40_44" || age == "45_49" || age == "50_54"){
           topType = "LongHairBigHair"
           accessoriesType = "Prescription02"
           hairColor = "Platinum"
           clotheType = "CollarSweater"
       }
       else if(age == "55+"){
           topType = "LongHairCurly"
           accessoriesType = "Prescription01"
           hairColor = "SilverGray"
           clotheType = "Overall"
           mouthType = "Twinkle"
       }
    }
    if(race == "American_Indian_Alaska_Native"){
       skinColor = "Tanned"
    }
    else if (race == "white") {
       skinColor = "Pale"
    }
    else if (race == "Black_sAfrican") {
       skinColor = "DarkBrown"
    }


   avatar_img.src = "https://avataaars.io/?avatarStyle=Circle&topType="+topType+"&accessoriesType="+accessoriesType+"&hairColor="+hairColor+"&facialHairType="+facialHairType+"&facialHairColor="+facialHairColor+"&clotheType="+clotheType+"&clotheColor=Heather&graphicType=Hola&eyeType=Default&eyebrowType="+eyebrowType+"&mouthType="+mouthType+"&skinColor="+skinColor



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
                document.getElementById("alcohol_percent").innerHTML = response.data.alcohol_probability + "%"
                document.getElementById("marijuana_percent").innerHTML = response.data.marijuana_probability + "%"
                document.getElementById("cocain_percent").innerHTML = response.data.cocain_probability + "%"

                // $('#elementId').append("<div id= 'alcohol_probability' class='skillbar clearfix' data-percent='"+response.data.alcohol_probability+"%'> <div class='skillbar-title' style='background: #2980b9;'><span>Alcohol</span></div> <div class='skillbar-bar' style='background: #3498db;'></div> </div>");

              jQuery('.skillbar').each(function(){
                     jQuery(this).find('.skillbar-bar').animate({
                        width:jQuery(this).attr('data-percent')
                    },2000);
                });

                if(rounded>0.561196927){
                 var chances = Math.round(rounded / 0.561196927)
                    if(chances==1){
document.               getElementById("inside-probability").innerHTML = "Your chances is equal the national average";
                    }else{
                        document.getElementById("inside-probability").innerHTML = "Your chances are "+ chances+ " times more than the national average";
                    //alert(rounded);
                    }

                }else{
                     var chances = Math.round(0.561196927 / rounded)
                    if(chances==1){
document.               getElementById("inside-probability").innerHTML = "Your chances is equal the national average";
                    }else {

                        document.getElementById("inside-probability").innerHTML = "Your chances are " + chances + " times less than the national average";
                    }
                }
//Alcohol===100379600/1,732,741=57.9311 
// Cokane=39188200/1,732,741=22.6163 
// Marijuana=67727000/1,732,741=69.0866
                var alcProb=response.data.alcohol_probability
                var marProb=response.data.marijuana_probability
                var cokProb=response.data.cocain_probability
                if(alcProb>57.93){
                    var chancesAlc = Math.round((alcProb*100)/(57.9311))/100
                    document.getElementById("alcoholNAText").innerHTML = "Your chances are "+chancesAlc+" times of the national average";
                }else{
                    var chancesAlc = Math.round((alcProb*100)/(57.9311))/100
                   document.getElementById("alcoholNAText").innerHTML = "Your chances are "+chancesAlc+" times of the national average";
                }

                if(marProb>22.6163 ){
                    var chancesMar = Math.round((marProb*100 )/22.6163 )/100
                    document.getElementById("marijuanaNAText").innerHTML = "Your chances are "+chancesMar+" times of the national average";
                }else{
                    var chancesMar = Math.round((marProb*100 )/22.6163 )/100
                    document.getElementById("marijuanaNAText").innerHTML = "Your chances are "+chancesMar+" times of the national average";
                }

                if(cokProb>69.0866){
                    var chancesCok = Math.round((cokProb*100)/69.0866)/100
                    document.getElementById("cokainNAText").innerHTML = "Your chances are "+chancesCok+" times of the national average";
                }else{
                    var chancesCok = Math.round((cokProb*100)/69.0866)/100
                    document.getElementById("cokainNAText").innerHTML = "Your chances are "+chancesCok+" times of the national average";
                }





                document.getElementById("container-speed").innerHTML = rounded + "%";
               // document.getElementById("inside-probability").innerHTML = "Your chances are "+ chances+ " times the national average";


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
    document.getElementById("description").innerHTML=val + " State Drug Analytics";

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