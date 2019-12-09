(function () {
    $.setInformation = {
        Confirm: function (title,Infomation) {
            GenerateHtml(title,Infomation);
            btnNo();
            // add(callback);
        }
    }
    //生成Html
    var GenerateHtml = function (title,Infomation) {
        var _html = "";
        _html += '<div id="mb_box"></div><div id="mb_con" style="padding-top:20px;max-width:400px;"><span id="mb_tit">' + title + '</span><a id="mb_ico">X</a>';
        _html += '<div class="col-lg-12" style="padding-bottom: 20px;padding-top:20px;width: 100%;margin: 0 auto">'
        _html += '<div style="padding: 20px">'+ Infomation +'</div>'
        _html +='</div>'
            +'</div>'
        console.info(_html)
        //必须先将_html添加到body，再设置Css样式
        $("body").append(_html);
        //生成Css
        GenerateCss();
    }

    //生成Css
    var GenerateCss = function () {
        // console.info("开始")
        $("#mb_box").css({ width: '100%', height: '100%', zIndex: '99999', position: 'fixed',
            filter: 'Alpha(opacity=60)', backgroundColor: 'black', top: '0', left: '0', opacity: '0.6'
        });
        $("#mb_con").css({ zIndex: '999999', width: '80%', position: 'fixed',//弹框的宽
            backgroundColor: 'White', borderRadius: '15px'
        });
        $("#mb_tit").css({ display: 'block', fontSize: '20px', color: '#009688', padding: '10px 15px',//字体颜色
            backgroundColor: 'white', borderRadius: '15px 15px 0 0',//顶部title颜色
            borderBottom: '3px solid #009688', fontWeight: 'bold'//线条颜色
        });
        $("#mb_msg").css({ padding: '20px', lineHeight: '20px',
            borderBottom: '1px dashed #DDD', fontSize: '13px'//虚线分界线颜色
        });
        $("#mb_ico").css({ display: 'block', position: 'absolute', right: '10px', top: '9px',
            border: '1px solid #009688', width: '18px', height: '18px', textAlign: 'center',//关闭图标外圈颜色
            lineHeight: '16px', cursor: 'pointer', borderRadius: '12px', fontFamily: '微软雅黑'
        });
        $("#mb_btnbox").css({ margin: '15px 0 10px 0', textAlign: 'center' });
        $("#mb_btn_ok,#mb_btn_no").css({ width: '85px', height: '30px', color: 'white', border: 'none' });
        $("#mb_btn_ok").css({ backgroundColor: '#009688' });//按钮颜色
        $("#mb_btn_no").css({ backgroundColor: '#009688', marginLeft: '20px' });//按钮颜色
        //右上角关闭按钮hover样式
        $("#mb_ico").hover(function () {
            $(this).css({ backgroundColor: '#009688', color: 'White' });//鼠标悬停效果
        }, function () {
            $(this).css({ backgroundColor: 'White', color: '#009688' });//鼠标离开之后效果
        });
        var _widht = document.documentElement.clientWidth;  //屏幕宽
        // var _height = document.body.clientHeight; //屏幕高
        var _height = '300px';
        var boxWidth = $("#mb_con").width();
        var boxHeight = $("#mb_con").height();
        // console.log(_widht)
        // console.log(document.body.clientHeight)
        // console.log(boxWidth)
        // console.log(boxHeight)
        //让提示框居中
        $("#mb_con").css({ top:"300px", left: (_widht - boxWidth) / 2 + "px" });
    }


    //取消按钮事件
    var btnNo = function () {
        $("#mb_btn_no,#mb_ico").click(function () {
            $("#mb_box,#mb_con").remove();
        });
    }
    /*var add = function (callback) {
        $("#mb_btn_ok").click(function () {
            console.log(JSON.stringify($("#addform").serializeArray()))
            $("#mb_box,#mb_con").remove();
            callback();
        });
    }*/
})();
