(function () {
    var eventData = {};
    $.AddSchedule = {
        Confirm: function (title, buttonText,isClass,event, callback,delBack) {
            eventData = event;
            GenerateHtml(title,buttonText,isClass);
            btnNo();
            btnOk(callback);

            if(delBack){
                $('#mb_btn_delete').removeClass("hide");
                btnDel(delBack);
            }
        }
    }
    //生成Html
    var GenerateHtml = function (title,buttonText,isClass) {
        var _html = "";
        _html += '<div id="mb_box"></div><div id="mb_con" style="padding-top:20px;max-width:400px"><span id="mb_tit" fontSize="30px">' + title + '</span>';
        _html += ' <form id="addform">'
            + '<div style="margin:0 auto; width: 90%; padding-top:40px" > '
            + '<input type="text" style="width: 100%;height:40px" fontSize="16px"; name="title" Placeholder="课程"  required="" />'
            + '</div>'
            + '<div style="margin:0 auto; width: 90%; padding-top:40px" > '
            + '<input type="text" style="width: 100%;height:40px" fontSize="16px"; name="description" Placeholder="描述"  required="" />'
            + '</div>'
            if(!isClass){
                _html += '<div style="margin:0 auto; width: 90%; padding-top:40px" > '
                    + '<input id="createTime"  class="form-control bg-light" name="startTime"  placeholder="启用时间" aria-label="Search" aria-describedby="basic-addon2" type="date" />'
                    + '</div>'
                    +'<div style="margin:0 auto; width: 90%; padding-top:40px" > '
                    + '<input id="endTime"  class="form-control bg-light" name="endTime"  placeholder="停用时间" aria-label="Search" aria-describedby="basic-addon2" type="date" />'
                    + '</div>'
            }

        _html += '</form>'
            + '<div id="mb_btnbox" style="padding:20px">'
            + '<button class="btn btn-info" id="mb_btn_no" type="button"><i>取消</i></button>'
            + '<button class="btn btn-primary" id="mb_btn_ok" style="margin: 20px" type="button"><i>'+buttonText+'</i></button>'
            + '<button class="btn btn-danger hide" id="mb_btn_delete" type="button"><i>删除</i></button>'
            + '</div>'
        ;
        //必须先将_html添加到body，再设置Css样式
        $("body").append(_html);
        //生成Css
        GenerateCss(isClass);
    }

    //生成Css
    var GenerateCss = function (isClass) {
        $("#mb_box").css({
            width: '100%', height: '100%', zIndex: '99999', position: 'fixed',
            filter: 'Alpha(opacity=60)', backgroundColor: 'black', top: '0', left: '0', opacity: '0.6'
        });
        $("#mb_con").css({
            zIndex: '999999', width: '80%', position: 'fixed',//弹框的宽
            backgroundColor: 'White', borderRadius: '15px'
        });
        $("#mb_tit").css({
            display: 'block', fontSize: '20px', color: '#009688', padding: '10px 15px',//字体颜色
            backgroundColor: 'white', borderRadius: '15px 15px 0 0',//顶部title颜色
            borderBottom: '3px solid #009688', fontWeight: 'bold'//线条颜色
        });
        $("#mb_msg").css({
            padding: '20px', lineHeight: '20px',
            borderBottom: '1px dashed #DDD', fontSize: '13px'//虚线分界线颜色
        });
        $("#mb_ico").css({
            display: 'block', position: 'absolute', right: '10px', top: '9px',
            border: '1px solid #1fc88d', width: '18px', height: '18px', textAlign: 'center',//关闭图标外圈颜色
            lineHeight: '16px', cursor: 'pointer', borderRadius: '12px', fontFamily: '微软雅黑'
        });
        $("#mb_btnbox").css({margin: '15px 0 10px 0', textAlign: 'center'});
        $("#mb_btn_ok,#mb_btn_no,#mb_btn_delete").css({width: '85px', height: '30px', color: 'white', border: 'none'});
        //$("#mb_btn_ok").css({ backgroundColor: '#1fc88d' });//按钮颜色
        //$("#mb_btn_no").css({ backgroundColor: '#1fc88d', marginLeft: '20px' });//按钮颜色
        //右上角关闭按钮hover样式
        $("#mb_ico").hover(function () {
            $(this).css({backgroundColor: '#1fc88d', color: 'White'});//鼠标悬停效果
        }, function () {
            $(this).css({backgroundColor: 'White', color: '#1fc88d'});//鼠标离开之后效果
        });
        var _widht = document.documentElement.clientWidth;  //屏幕宽
        var _height = document.documentElement.clientHeight; //屏幕高
        var boxWidth = $("#mb_con").width();
        var boxHeight = $("#mb_con").height();
        //console.log(_height)
        //让提示框居中
        $("#mb_con").css({top: (_height - boxHeight) / 2 + "px", left: (_widht - boxWidth) / 2 + "px"});

        //判断是否需要注入数据
        if(eventData){
            updateData(isClass);
        }
    }
    //取消按钮事件
    var btnNo = function () {
        $("#mb_btn_no,#mb_ico").click(function () {
            $("#mb_box,#mb_con").remove();
        });
    }
    var btnOk = function (callback) {
        $("#mb_btn_ok").click(function () {
            callback();
            $("#mb_box,#mb_con").remove();
        });
    }
    var btnDel = function (delBack) {
        $('#mb_btn_delete').click(function () {
            delBack();
            $("#mb_box,#mb_con").remove();
        })
    }
    //编辑事件
    var updateData = function (isClass) {
        $("input[name='title']").val(eventData.title);
        $("input[name='description']").val(eventData.description);
        if(!isClass){
            $("input[name='startTime']").val(eventData.created_time);
            $("input[name='endTime']").val(eventData.end_recurring_period);
        }
    }
})();
