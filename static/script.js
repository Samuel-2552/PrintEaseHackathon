
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
            url: 'service/upload.php',
            type: 'POST',
            data: fd,
            processData: false,
            contentType: false,
            success: function () {
                containerProg.option('displayNumber', false);
                msgHolder.show().html('File upload done.');
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
            }
        });

    }

});
function next1() {
    document.getElementById("ques1").hidden = false;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;

}
function next2() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = false;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;

}
function next3() {
    console.log("next3 is working")
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = false;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;
}
function next4() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = false;
    document.getElementById("scan").hidden = true;

}


function back1() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = false;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;
}
function back2() {
    document.getElementById("ques1").hidden = false;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;
}
function back3() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = false;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;
}
function back4() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = false;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = true;
}
function checkout() {
    document.getElementById("ques1").hidden = true;
    document.getElementById("ques2").hidden = true;
    document.getElementById("upload").hidden = true;
    document.getElementById("ques3").hidden = true;
    document.getElementById("bill").hidden = true;
    document.getElementById("scan").hidden = false;
}