(function () {
    $.SendQuiz = {
        Confirm: function (title,questionInfo,callback) {
            GenerateHtml(title,questionInfo);
            btnNo();
            btnLook();
            add(callback);
        }
    }
    //生成Html
    var GenerateHtml = function (title,questionInfo) {
        var _html = "";
        _html += '<div id="mb_box"></div><div id="mb_con" style="padding-top:20px;max-width:400px;"><span id="mb_tit">' + title + '</span><a id="mb_ico">X</a>';
        _html += '<div class="col-lg-12" style="padding-top: 40px;padding-bottom: 40px;width: 90%;margin: 0 auto">'
            +'<table width="100%" cellspacing="10px style="">'
            +'<tr>'
            +'<th width="50%">试卷名称：</th>'
            +'<th width="50%">'
        if(questionInfo.title){
            _html+=questionInfo.title
        }else{
            _html+=''
        }

        _html+='</th>'
            +'</tr>'
            +'<tr>'
            +'<th width="50%">测试编号：</th>'
            +'<th width="50%">'
        if(questionInfo.id){
            _html+=questionInfo.id
        }else{
            _html+='暂无'
        }
        _html+='</th>'
            +'</tr>'
            +'<tr>'
            +'<th width="50%">班级：</th>'
            +'<th width="50%">'+questionInfo.cls+'</th>'
            +'</tr>'
            +'<tr>'
            +'<th width="50%">科目：</th>'
            +'<th width="50%">'+questionInfo.subject+'</th>'
            +'</tr>'
            +'<tr>'
            +'<th width="50%"></th>'
            +'<th width="50%"></th>'
            +'</tr>'
            +'</table>'
            +'<div id="mb_btnbox">'
                //+' <button class="btn btn-primary" id="mb_btn_ok" style="margin-right: 20px" type="button"><i>导出PDF</i></button>'
                //+'<button class="btn btn-primary" id="mb_btn_no" type="button"><i>查看试卷</i></button>'
            +'<input id="mb_btn_ok" type="button" style="border-radius:5px;" value="导出PDF" />'
            +'<input id="mb_btn_look" type="button"  style="border-radius:5px;" value="查看试卷" />'
            + '</div>'
            +'</div>'
            +'</div>'
        
        //必须先将_html添加到body，再设置Css样式
        $("body").append(_html);
        //生成Css
        GenerateCss();
    }

    //生成Css
    var GenerateCss = function () {
        $("#mb_box").css({ width: '100%', height: '100%', zIndex: '99999', position: 'fixed',
            filter: 'Alpha(opacity=60)', backgroundColor: 'black', top: '0', left: '0', opacity: '0.6'
        });
        $("#mb_con").css({ zIndex: '999999', width: '80%', position: 'fixed',//弹框的宽
            backgroundColor: 'White', borderRadius: '15px'
        });
        $("#mb_tit").css({ display: 'block', fontSize: '20px', color: '#1fc88d', padding: '10px 15px',//字体颜色
            backgroundColor: 'white', borderRadius: '15px 15px 0 0',//顶部title颜色
            borderBottom: '3px solid #1fc88d', fontWeight: 'bold'//线条颜色
        });
        $("#mb_msg").css({ padding: '20px', lineHeight: '20px',
            borderBottom: '1px dashed #DDD', fontSize: '13px'//虚线分界线颜色
        });
        $("#mb_ico").css({ display: 'block', position: 'absolute', right: '10px', top: '9px',
            border: '1px solid #1fc88d', width: '18px', height: '18px', textAlign: 'center',//关闭图标外圈颜色
            lineHeight: '16px', cursor: 'pointer', borderRadius: '12px', fontFamily: '微软雅黑'
        });
        $("#mb_btnbox").css({ margin: '15px 0 10px 0', textAlign: 'center' });
        $("#mb_btn_ok,#mb_btn_look").css({ width: '85px', height: '30px', color: 'white', border: 'none' });
        $("#mb_btn_ok").css({ backgroundColor: '#1fc88d' });//按钮颜色
        $("#mb_btn_look").css({ backgroundColor: '#1fc88d', marginLeft: '20px' });//按钮颜色
        //右上角关闭按钮hover样式
        $("#mb_ico").hover(function () {
            $(this).css({ backgroundColor: '#1fc88d', color: 'White' });//鼠标悬停效果
        }, function () {
            $(this).css({ backgroundColor: 'White', color: '#1fc88d' });//鼠标离开之后效果
        });
        var _widht = document.documentElement.clientWidth;  //屏幕宽
        var _height = document.documentElement.clientHeight; //屏幕高
        //console.info(_height)
        var boxWidth = $("#mb_con").width();
        var boxHeight = $("#mb_con").height();
        // console.log(_widht)
        // console.log(document.body.clientHeight)
        // console.log(boxWidth)
        // console.log(boxHeight)
        //让提示框居中
        $("#mb_con").css({ top: (_height-boxHeight)/2 + "px", left: (_widht - boxWidth) / 2 + "px" });
    }
    //取消按钮事件
    var btnNo = function () {
        $("#mb_ico").click(function () {
            $("#mb_box,#mb_con").remove();
        });
    }
    var add = function (callback) {
        $("#mb_btn_ok").click(function () {
            console.log(JSON.stringify($("#addform").serializeArray()))
            $("#mb_box,#mb_con").remove();
            callback();
        });
    }
    var btnLook = function () {
        $('#mb_btn_look').click(function () {
            window.location.href="http://47.110.253.251/abc/teacher/my-quizes/";
        })
    }
})();
