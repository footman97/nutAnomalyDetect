// 加载完成后执行
$(document).ready(function(){

    // method2
    $("#input-704").fileinput({
        language: 'zh', //设置语言
        allowedFileExtensions: ['xlsx', 'xls'],  //接收的文件后缀
        uploadUrl:  "/upload",  //上传的地址
        minFileCount: 1,
        maxFileCount: 100,
        uploadAsync: false, // 不使用异步上传 数组接收文件
        showUpload: true, //是否显示上传按钮

        showRemove : true, //显示移除按钮
        showPreview : true, //是否显示预览

    });

    // //异步上传返回结果处理
    // $("#input-704").on("fileuploaded", function (event, data, previewId, index) {
    //     var response = data.response;
    //     alert(response.message);
    //
    // });

    //同步上传返回结果处理
    $("#input-704").on("filepreupload", function (event, data, previewId, index) {
        // var response = data.response;
        // alert(response.message);

        $('#prompt-1').innerText("等待返回计算结果....");

    });



});


// method1 without bootstrap-inputfile
$("#ud").click(function(){

    alert("submit begin!");

    var type = "file";          //后台接收时需要的参数名称，自定义即可
    var id = "cert";            //即input的id，用来寻找值
    var formData = new FormData();
    formData.append(type, $("#"+id)[0].files[0]);    //生成一对表单属性
    $.ajax({
        type: "POST",           //因为是传输文件，所以必须是post
        url: '/upload',         //对应的后台处理类的地址
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data);
        }
    });
});

