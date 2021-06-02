let videoHeight = 480
let videoWidth = 480
var outputCanvas = null;

var faceCascade = null;

var streaming = null;
var get_face_true = 0;
window.predict_img = "#predict-img";
window.input_img = "#input_img";
window.cv = null;
function run() {
    window.cv = cv;

    $("#_getmediaDevices").click(function () {

        startCamera();
        window.g_src = undefined
        outputCanvas = document.getElementById("outputCanvas");
        faceCascade = new cv.CascadeClassifier();
        faceCascade.load("face.xml");
        window.cap = new cv.VideoCapture(video);
        window.src = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
        window.gray = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC1);
        // startCamera();


        setTimeout(function () {
            requestAnimationFrame(detectFace)
        }, 1);


    });


    $(".face-btn").click(function () {

        window.predict_img = "#" + $(this).attr("data-predict_img");
        window.input_img = "#" + $(this).attr("data-input_img");
        layer.open({
            type: 1,
            content: $("#face").text(),

            success() {


                window.g_src = undefined

                outputCanvas = document.getElementById("outputCanvas");
                faceCascade = new cv.CascadeClassifier();
                faceCascade.load("face.xml");
                cap = new cv.VideoCapture(video);
                src = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
                gray = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC1);
                startCamera();
                requestAnimationFrame(detectFace)

            }, area: ["510px", "540px"],
            end: function () {
                if (streaming) {
                    streaming.getTracks()[0].stop();
                    streaming = null;
                }
            }
        });


    })
window.cv_ok = true

}

async function startCamera() {
    let video = document.getElementById("video");
    let stream = await navigator.mediaDevices.getUserMedia({
        video: {
            width: {
                exact: videoWidth
            },
            height: {
                exact: videoHeight
            }
        },
        audio: false
    })
    video.srcObject = stream;
    streaming = stream;
    video.play();
}

function detectFace() {
    // Capture a frame
    if (!cap) {
        requestAnimationFrame(detectFace)
        return
    }
    cap.read(src);

    // Convert to greyscale
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);


    // Downsample
    let downSampled = new cv.Mat();
    cv.pyrDown(gray, downSampled);
    cv.pyrDown(downSampled, downSampled);

    // Detect faces
    let faces = new cv.RectVector();
    faceCascade.detectMultiScale(downSampled, faces);

    // Draw boxes
    let size = downSampled.size();
    let xRatio = videoWidth / size.width;
    let yRatio = videoHeight / size.height;

    for (let i = 0; i < faces.size(); ++i) {
        let face = faces.get(i);
        console.log(face.x * xRatio, face.y * yRatio);
        get_face_true++;

        let point1 = new cv.Point(face.x * xRatio, face.y * yRatio);
        let point2 = new cv.Point((face.x + face.width) * xRatio, (face.y + face.height) * xRatio);
        cv.rectangle(src, point1, point2, [255, 0, 0, 255])
    }
    // Free memory
    downSampled.delete();
    faces.delete();
    cv.imshow(outputCanvas, src);
    // Show image

    var img_url = outputCanvas.toDataURL("image/png")
    window.g_src = img_url;

    layer.closeAll();
    $(input_img).val(window.g_src);
    $(predict_img).attr("src", window.g_src);


    get_face_true = 0;
    if (check_loop == false) {
        outputCanvas = null;
        cap = null;
        faceCascade = null;
        src = null;
        gray = null;

        get_face_true = 0;
        return

    }

    requestAnimationFrame(detectFace)


}

// Config OpenCV
var Module = {
    locateFile: function (name) {
        let files = {
            "opencv_js.wasm": '/static/opencv_js.wasm'
        }
        return files[name]
    },
    preRun: [() => {
        Module.FS_createPreloadedFile("/", "face.xml", "/static/haarcascade_frontalface_default.xml",
            true, false);
    }],
    postRun: [
        run
    ]
};