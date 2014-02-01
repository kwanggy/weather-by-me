$(document).ready(
function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition);
    }
  else{x.innerHTML="Geolocation is not supported by this browser.";}
  });

function showPosition(position)
  {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    console.log(lat); 
    console.log(lon);
  }//geting user's lantitude, longitude;



var woeid = '2459115';//hardcode New York need to be fixed
var $url = "http://query.yahooapis.com/v1/public/yql?callback=?";

$(document).ready(function(){
$.getJSON($url, {
    q: "select * from xml where url=" +
       "\"http://weather.yahooapis.com/forecastrss?w=" + woeid + "\"",
    format: "json"
  }, function (data) {
    var r = data.query.results.rss.channel;
    console.log(r);
    html = '<h2 style="color: #444; font-size:2.0em; display: block;-webkit-margin-before: 0.83em;-webkit-margin-after: 0.83em;-webkit-margin-start: 0px;-webkit-margin-end: 0px;font-weight: bold;">'+r.location.city+', '+r.location.region+'</h2>';
    html += '<img style="float:left;" width="250px" height="200px" src="'+'http://l.yimg.com/a/i/us/nws/weather/gr/'+r.item.condition.code +'n.png'+'">';
    html += '<p style="display: block;-webkit-margin-before: 1em;-webkit-margin-after: 1em;-webkit-margin-start: 0px;-webkit-margin-end: 0px; font-size:40px;color:#444;">'+r.item.condition.temp+'&deg; '+r.units.temperature+'<br /><span>'+r.item.condition.text+'</span></p>';
    $("#test").html(html);
  }
);
});
