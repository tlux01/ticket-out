
var colorGen = $(".aColor");

// creates variable number of random colors
      for(var i=0; i<colorGen.length; i++){
        var color = ranColor();
        colorGen[i].style.background = color;
      };

// $(".btn-primry").click(function (){
// 	$(this).css("background-color", ranColor());

// });






function ranColorGenerator(){
	var colorGen = $(".aColor");

// creates variable number of random colors
      for(var i=0; i<colorGen.length; i++){
        var color = ranColor();
        colorGen[i].style.background = color;
      };
}

function backgroundSwitch(y){
	$("body").css("backgroundColor", y)
	$(".container").css("backgroundColor", y)
	$(".col").css("backgroundColor", y)
}


function getColor(e){
	var prefColor = $(e);
	return (prefColor.css("background-color"));
}

function generateSimilar(x){
	var colour = x;
	colorGen[0].style.background = colour;
	var slicer = colour.lastIndexOf(" ", "r")
	var theB = colour.slice(slicer+1, colour.length-1)
	var initialPeice = colour.slice(0, slicer);
	for(i=1; i < 6; i++){
		theB = 20 + (+theB)
		if (theB <= 250){
			theStringColor = initialPeice +" " + theB + ")"
			colorGen[i].style.background = theStringColor;
		} else{
			theB = (+theB) - 120
			theStringColor = initialPeice +" " + theB + ")"
			colorGen[i].style.background = theStringColor;

		}
		

	}
}
//creates random color
function ranColor() {
        var r = Math.floor(Math.random() * 256); 
        var g = Math.floor(Math.random() * 256);
        var b = Math.floor(Math.random() * 256);
        var color = "rgb( " + r + ", " + g + ", " + b + ")";
        return color
    }
      