$(document).ready(function() {
    // 訊息視窗彈出
    function openMsgWindow(type, title, content, callback=null) {
        $('#msg_window').addClass(type);
        $('#msg_window').find('.title').html(title);
        $('#msg_window').find('.content').html(content);
        $('#msg_window').addClass('show');

        $('#msg_window').on('click', '.btn_ok, .btn_yes', function(e) {
            e.preventDefault();
            $('#msg_window').removeClass(type);
            $('#msg_window').removeClass('show');
            if (callback != null) callback();
        })

        $('#msg_window').on('click', '.btn_no', function(e) {
            e.preventDefault();
            $('#msg_window').removeClass(type);
            $('#msg_window').removeClass('show');
            return;
        })
    }

    // 表單驗證
    function checkRequired(form) {
        var pass = true;

        // check text input
        form.find('.required').each(function() {
            if (!$(this).val()) {
                $(this).focus();
                pass = false;
                return false
            }
        });

        return pass
    }

    // ajax表單送出
    function postAjax(url, data, callback) {
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: function(rep) {
                callback(rep)
            }
        })
    }

    // 切換收入/支出
    $('#chicken_management, #hotpot_management').on('click', 'input[name="type"]', function(e) {
        let cat = $(this).val()
        if (cat == 'income') {
            $('label[for="income"]').html("<i class='fa-solid fa-check'></i>收入");
            $('label[for="expense"]').html('支出');
            $('.income_item').removeClass('hide');
            $('.income_item').find('.item_required').addClass('required');
            $('.expense_item').addClass('hide');
            $('.expense_item').find('.item_required').removeClass('required');
        } else if (cat == 'expense') {
            $('label[for="income"]').html('收入');
            $('label[for="expense"]').html("<i class='fa-solid fa-check'></i>支出");
            $('.income_item').addClass('hide');
            $('.income_item').find('.item_required').removeClass('required');
            $('.expense_item').removeClass('hide');
            $('.expense_item').find('.item_required').addClass('required');
        }
    })

    // 切換表單類別
    $('#system_management').on('click', 'input[name="type"]', function(e) {
        let cat = $(this).val()
        $('label[for="type_chicken"]').html('馥香雞');
        $('label[for="type_hotpot"]').html('日料');
        $('label[for="type_home"]').html('家庭');
        switch (cat) {
            case 'chicken':
                $('label[for="type_chicken"]').html("<i class='fa-solid fa-check'></i>馥香雞");
                break;
            case 'hotpot':
                $('label[for="type_hotpot"]').html("<i class='fa-solid fa-check'></i>日料");
                break;
            case 'home':
                $('label[for="type_home"]').html("<i class='fa-solid fa-check'></i>家庭");
                break;
          }
    })

    // 送出-收入支出表單
    $('#chicken_management, #hotpot_management, #expense_management').on('click', '.submit_btn, .continue_btn', function(e) {
        e.preventDefault();

        let next = $(this).hasClass('continue_btn') ? 'reload' : 'home';

        //表顛驗證
        let form = $(this).closest('form');
        var result_pass = checkRequired(form);
        if (!result_pass) {
            openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
            return;
        }

        // 送出
        let url = form.attr('action');
        let data = form.serialize();
        postAjax(url, data, function(rep) {
            if (next == 'reload') {
                window.location.reload();
            } else {
                let home_url = $('.cancel_btn').data('url');
                window.location.href = home_url;
            }
        })
    })

    // 送出-設定表單
    $('#system_management').on('click', '.submit_btn, .continue_btn', function(e) {
        e.preventDefault();
        let next = $(this).hasClass('continue_btn') ? 'reload' : 'home';

        //表顛驗證
        let form = $(this).closest('form');
        var result_pass = checkRequired(form);
        if (!result_pass) {
            openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
            return;
        }

        // 送出
        let url = form.attr('action');
        let data = form.serialize();
        postAjax(url, data, function(rep) {
            if (next == 'reload') {
                window.location.reload();
            } else {
                let back_url = $('.cancel_btn').attr('href');
                let new_url = back_url.split('?')[0]+"?cat="+rep.type;
                window.location.href = new_url;
            }
        })
    })

    // 刪除單筆資料-報表
    $('#report_management').on('click', '.delete_btn', function(e) {
        let form = $(this).closest('form');
        let url = form.attr('action');
        let data = form.serialize();

        openMsgWindow('confirm', '確定要刪除資料嗎?', '刪除後資料將不會保留唷!', function() {
            postAjax(url, data, function(rep) {
               window.location.reload();
            })
        })
    })

    // 刪除單筆資料-設定
    $('#system_management').on('click', '.delete_btn', function(e) {
        let form = $(this).closest('form');
        let url = form.attr('action');
        let data = form.serialize();

        openMsgWindow('confirm', '確定要刪除資料嗎?', '確認刪除的話，資料庫中關於這個類別的帳款都會一併刪除唷!', function() {
            postAjax(url, data, function(rep) {
               window.location.reload();
            })
        })
    })

    // 返回
    $('#chicken_management, #hotpot_management, #expense_management').on('click', '.cancel_btn', function(e) {
          e.preventDefault();
          let url = $(this).data('url');
          window.location.href = url;
    })

    // 切換顏色設定
    $('#system_management').on('click', '.color_btn', function(e) {

        let form = $(this).closest('form');
        let value = $(this).prev().val();
        form.find('input[name="_color"]').val(value);

        let url = form.attr('action');
        let data = form.serialize();
        postAjax(url, data, function(rep) {
            window.location.reload();
        })
    })

    // 登入送出表單
    $('#login_page').on('click', '.btn_ok', function(e) {

        let form = $(this).closest('form');

        //表顛驗證
        var result_pass = checkRequired(form);
        if (!result_pass) {
            openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
            return;
        }

        let url = form.attr('action');
        let data = form.serialize();
        postAjax(url, data, function(rep) {
            if (rep.status)
                window.location.href = rep.next;
            else {
              switch (rep.error) {
                  case -1:
                      openMsgWindow('remind', '資料不完整', '要填寫完整才能送出唷!', function(e) {});
                      break;
                  case -2:
                      openMsgWindow('remind', '資料不正確', '找不到用戶，請確認一下帳號密碼是否輸入錯誤!', function(e) {});
                      break;
              }

            }
        })
    })
    $('#login_page').on('keyup', '.required',function(e) {
        if (e.keyCode === 13) {
            $('#login_page').find('.btn_ok').click();
        }
    })
});