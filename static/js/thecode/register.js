$(
    () => {
        // 点击刷新验证码
        $('#piccode').click(function () {
                $(this).attr('src', '/veri/image_code?rand=' + Math.random());
            }
        )
    }
);

// 定义状态变量

let isUsernameReady = false,        // 昵称状态
    isPasswordReady = false,        // 密码状态
    isEmailReady = false,           // 邮箱
    isEmCodeReady = false;         // 邮箱验证码

// 焦点离开nickname 校验
// 昵称校验 onblur
let $username = $('#nickname');
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

    // 发送ajax
    $.ajax({
        url: '/veri/check=' + $sUsername + '/',
        type: 'GET',
        dataType: 'JSON',
        success: function (res) {
            if (res['data']['count'] !== 0) {
                message.show('昵称已被注册')
            } else {
                isUsernameReady = true;
                message.show('该昵称可以正常使用')
            }
        },
        error: function () {
            message.show('服务器超时，请重试')
        }
    })
}


// 密码
let $password = $('#pwd'),
    $passwordRepeat = $('input[name="password_repeat"]');

$password.blur(password_format);
$passwordRepeat.blur(password_equal);

// 密码格式校验
function password_format(){
    if (!(/^.{5,20}$/).test($password.val())){
        message.show('密码格式必须为5~20位字符串')
    }
}
// 两次密码是否一致
function password_equal(){
    isPasswordReady = false;
    if (!$passwordRepeat.val()){
        message.show('密码不能为空')
        return
    }
    if (!(/^.{5,20}$/).test($password.val())){
        message.show('密码格式必须为5~20位字符串')
        return
    }
    if ($password.val() !== $passwordRepeat.val()){
        message.show('两次输入的密码不正确，请重新输入')
    }else{
        isPasswordReady = true
    }

}


// 焦点离开验证邮箱 1.获得邮箱 2.ajax发送
let $email = $("#email");
$email.blur(send_email);

function send_email() {
    isEmailReady = false;
    // 获取email
    $semail = $email.val();
    if (!$semail) {
        message.show('你的邮箱是空的吗');
        return
    } else if (!(/^.*?@.*?\.com|cn$/).test($semail)) {
        message.show('你觉得邮箱格式对了吗');
        return
    }

    // 发送ajax
    $.ajax({
        url: '/veri/email/',
        type: 'POST',
        data:{"email": $semail},
        dataType: 'JSON',
    })
        .done(function (res) {
            if (res['data']['count'] !== 0) {
                message.show('邮箱已被注册')
            } else {
                isEmailReady = true;
                message.show("邮箱可以使用")
            }
        })
        .fail(
            function () {
                message.show('服务器超时请重试')
            }
        )
}

// 发送邮箱验证码
let $mailcode = $('.getmailcode');
$mailcode.click(smsButton);

function smsButton(e) {
    e.preventDefault();
    // 取得邮箱
    let $sMailCode = $("#email").val();
    // 取得图形验证码
    let $sImageCode = $('#image_code').val();
    if (!$sImageCode) {
        message.show('图形验证码不能为空');
        return
    }
    if (!isEmailReady) {
        send_email();
        return
    }
    // 发送ajax
    $.ajax({
        url: '/veri/sendmail/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            email: $sMailCode,
            image_code: $sImageCode
        }
    })
        .done(function (res) {
            if (res['errno'] != 0) {
                message.show(res['errmsg'])
            } else {
                $mailcode.attr('disabled', true);
                var num = 60;
                let t = setInterval(function () {
                    $mailcode[0].innerText = num;
                    if (num === 1) {
                        clearInterval(t);
                        $mailcode[0].innerText = '获取邮箱验证码';
                        $mailcode.removeAttr('disabled');
                    }
                    num--;
                }, 1000)
            }
        })
        .fail(
            function () {
                message.show('服务器超时请重试')
            }
        )
}

// 注册功能
let $registerBtn = $('input[type="submit"]');
$registerBtn.click(registerFn);

let $em_input = $('input[name="mailcode"]')
$em_input.blur(emInput)

function emInput() {
    isEmCodeReady = false;

    if ($em_input.val()){
        isEmCodeReady = true
    }else{
        message.show('请输入邮箱验证码');
    }
}

function registerFn(e) {
    e.preventDefault();

    if (!isUsernameReady) {
        checkUsername();
        return
    } else if (!isPasswordReady) {
        password_equal();
        return;
    } else if (!isEmailReady) {
        send_email();
        return
    } else if (!isEmCodeReady) {
        emInput();
        return
    }

    $.ajax({
        url: '/thecode/098f6bcd4621d373cade4e832627b4f6/',
        type: 'POST',
        dataType: 'JSON',
        data: {
            nickname: $sUsername,
            password: $password.val(),
            password_repeat: $passwordRepeat.val(),
            mailcode: $('input[name="mailcode"]').val(),
            email: $semail

        }
    })
        .done(function (res) {
            if (res['errno'] != 0) {
                message.show(res['errmsg'])
            } else {
                message.show('注册成功，即将跳转')
                // 跳转到登录页面
                setTimeout(()=>{
                    window.location.href = '/thecode/'
                }, 1500)
            }
        })
        .fail(
            function () {
                message.showError('服务器超时请重试')
            }
        )
}