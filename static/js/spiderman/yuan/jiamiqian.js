var screenWidth = window.screen.width;
// 定义一些默认参数
let
   iPage = 1,           // 默认当前页数
   iTotalPage = 0,      // 默认总页数
   isLoadData = true;   // 是否在加载数据

load_data();
// 点击点到最后一个的时候加载新的5个


$(document).on('click', '.slick-prev', function () {
    let $order = Number($('.slick-active').attr("order"));
    if ($order === 0){
        if (!isLoadData){
            isLoadData = true;
            if (iPage < iTotalPage){
                iPage += 1;
                load_data();
            }else{
                console.log("已加载全部内容");
            }
        }
    }
});


// 初始化加载n个
function load_data(){
    // 创建请求参数字典
    let sDataParams = {
        'page': iPage
    };

    $.ajax({
        url: "data/",
        type: "GET",
        data: sDataParams,
        dataType: "json"
    })
        .done(function (res) {
            if (res['errno']==="0"){
                iTotalPage = res['data']['total_pages'];
                if (iPage === 1){
                    $(".slide-container").html("")
                }
                res.data.spider.forEach(function(one_data){
                    $t_data = one_data.encrypt_data;
                    $t_data2 = '';
                    for(let i=0;i<$t_data.length;i++){
                        $t_data2 += String.fromCharCode($t_data.charAt(i).charCodeAt()-2);
                    }
                let content = `
            <div class="wrapper" order="${one_data.order}">
                <div class="clash-card">
                    <div class="clash-card__image">
                        <img src="/media/${one_data.image_url}" alt=""/>
                        <div class="context" style="width: 200px;font-family: 'Arial g'">
                            <p>${one_data.false_data}</p>
                            <br><br><br><br>
                            <code>{"${one_data.data_index}": "${$t_data2}" }</code>
                            <br>
                            <p style="text-align: right">第 ${one_data.order} 页</p>
                        </div>
                    </div>
                </div>
            </div>
                `;
                $(".slide-container").append(content);
                $(".slide-container")[0].slick.refresh();
                isLoadData = false;

            });
                let $slide = $('.slick-slide').length-2;
                console.log("左滑加载，已加载的条数："+$slide+'\t恭喜你回到第5页，继续努力吧')
        }else{
                console.log('有点莫名其妙的错误')
            }
        })
        .fail(function () {
            isLoadData = false;
            console.log('皮卡丘发现了你');
        })
}
