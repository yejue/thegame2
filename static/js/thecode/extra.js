var $siqi = $(".siqi")

$siqi.click(switch_bd);

function switch_bd() {
    $("body").css("background", "#EFBFE4")
        $
            .ajax({
                url: 'url=register',
                type:"GET",
                contentType: "application/json; charset=utf-8"
            })
            .done(function (res) {
                if(res["errno"] === "0"){
                    console.log(res["data"]["url"])
                }else if(res["errno"] === "4103"){
                    message.show("憨憨")
                }
            })
            .fail(function () {
                message.show("卡炸了")
            })

}

let isUsernameReady = false,        // 昵称状态
    isPasswordReady = false;         // 密码状态



// 焦点离开nickname 校验
// 昵称校验 onblur
let $username = $('input[name="nickname"]');
$username.blur(checkUsername);

function checkUsername() {
    isUsernameReady = false;
    // 取得昵称
    $sUsername = $username.val();

    if (!$sUsername) {
        message.show('昵称不能为空');
        return
    } else if (!(/^\w{2,20}$/).test($sUsername)) {
        message.show('请输入2~20位的昵称');
        return
    }
    isUsernameReady = true;
}

// 焦点离开password 校验
// 密码校验 onblur
let $password = $('input[name="password"]');
$password.blur(checkPwd);

function checkPwd() {
    isPasswordReady = false;
    // 取得密码
    $sPassword = $password.val();

    if (!$sPassword) {
        message.show('密码不能为空');
        return
    }
    isPasswordReady = true;
}

// 登录
let $loginBtn = $("input[type=submit]");
$loginBtn.click(loginFn);

function loginFn(e) {
    e.preventDefault();
    if (window.navigator.webdriver){
        window.location.replace("https://blog.csdn.net/qq_39177678");
    }
    if (!isUsernameReady) {
        checkUsername();
        return
    } else if (!isPasswordReady) {
        checkPwd();
        return;
    }
    $.ajax({
        url: '/thecode/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            nickname: $sUsername,
            password: $password.val(),
            rand: Math.random().toString()
        }
    })
        .done(function (res) {
            if (res['errno'] != 0) {
                message.show(res['errmsg'])
            } else {
                message.show('世界因你而改变');
                // 跳转到主页
                setTimeout(()=>{
                    window.location.href = '/spider/spiderdata'
                }, 1500)
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}