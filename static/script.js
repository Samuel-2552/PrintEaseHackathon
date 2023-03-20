
$(document).ready(function () {

    //file upload example
    var container = $('#indicatorContainerWrap'),
        msgHolder = container.find('.rad-cntnt'),
        containerProg = container.radialIndicator({
            radius: 100,
            percentage: true,
            displayNumber: false
        }).data('radialIndicator');


    container.on({
        'dragenter': function (e) {
            msgHolder.html("Drop here");
        },
        'dragleave': function (e) {
            msgHolder.html("Click / Drop file to select.");
        },
        'drop': function (e) {
            e.preventDefault();
            handleFileUpload(e.originalEvent.dataTransfer.files);
        }
    });

    $('#prgFileSelector').on('change', function () {
        handleFileUpload(this.files);
    });
    function handleFileUpload(files) {
        msgHolder.hide();
        containerProg.option('displayNumber', true);

        var file = files[0],
            fd = new FormData();

        fd.append('file', file);


        $.ajax({
            url: '/upload-file',
            type: 'POST',
            data: fd,
            processData: false,
            contentType: false,
            success: function (res) {
                containerProg.option('displayNumber', false);
                msgHolder.show().html('File upload done.');
                console.log(res);
            },
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                //Upload progress
                xhr.upload.addEventListener("progress", function (e) {

                    if (e.lengthComputable) {
                        var percentComplete = (e.loaded || e.position) * 100 / e.total;
                        containerProg.animate(percentComplete);
                        setTimeout(succupload, 2000);


                    }
                }, false);
                function succupload() {
                    let msg = `<span style="color:whitesmoke;">File <u><b>${file.name}</b></u> has been uploaded successfully.</span>`;
                    feedback.innerHTML = msg;
                    document.getElementById("next1").hidden = false;

                }
                return xhr;
                console.log(res);
            }

        });
    }

});

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }

  function showPosition(position) {
    document.getElementById("latitude").innerHTML = position.coords.latitude;
    document.getElementById("longitude").innerHTML = position.coords.longitude;
    var myView = new ol.View({
    center: ol.proj.fromLonLat([position.coords.longitude,  position.coords.latitude]),
    zoom: 18
  });
  
  var marker = new ol.Feature({
    geometry: new ol.geom.Point(
      ol.proj.fromLonLat([position.coords.longitude,  position.coords.latitude])
    )
  });
  
  var vectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: [marker]
    }),
    style: new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: 'https://openlayers.org/en/v4.6.5/examples/data/icon.png'
      })
    })
  });
  
  var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      }),
      vectorLayer
    ],
    view: myView
  });
    output();

  }

  function output() {
    const latitude = document.getElementById('latitude').textContent;
    const longitude = document.getElementById('longitude').textContent;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/update-location', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.send(JSON.stringify({ latitude: latitude, longitude: longitude }));
    xhr.onload = function () {
      const responseText = this.responseText;
      // console.log("response from app.py = "+responseText)
      if (responseText == "Success") {
        document.getElementById("show_shops").hidden = false;
      }

    };
  }

  function show_upload() {
    document.getElementById("before_location").hidden = true;
    document.getElementById("show_shops").hidden = true;
    document.getElementById("after_location").hidden = false;
  }

  function a1() {
    document.getElementById("ques1").hidden = false;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
  }
  function a2() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = false;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;

  }
  function a3() {
    console.log("next3 is working")
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = false;
  }
  function b1() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = false;
    document.getElementById("ques3").hidden = true;
  }
  function b2() {
    document.getElementById("ques1").hidden = false;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
  }
  function b3() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = false;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
  }
  if (window.performance && window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
    window.location = "{{ip}}";
  }
  function closePopup() {
    // Hide the pop-up window and overlay
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
  }