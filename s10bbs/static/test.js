$('#div_digg .action').click(function () {
        var is_up = $(this).hasClass("diggit");
        var article_id = $('.info').attr('acd_id');
        console.log(article_id);


        $.ajax({
            url:'/blog/up_down/',
            type:'post',
            data:{
                is_up:is_up,
                article_id:article_id,
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),

            },


            success:function (data) {
                if (data.state){

                        if(is_up){
                            var val=$("#digg_count").text();
                            val=parseInt(val)+1;
                            $("#digg_count").text(val);
                        }else {
                            var val=$("#bury_count").text();
                            val=parseInt(val)+1;
                            $("#bury_count").text(val);
                        }
                   }
                   else {    // 重复提交

                    if (data.fisrt_action) {
                        $("#digg_tips").html("您已经推荐过");
                    } else {
                        $("#digg_tips").html("您已经反对过");
                    }

                    setTimeout(function () {
                        $("#digg_tips").html("")
                    }, 1000)
                }
            }
        })
    });