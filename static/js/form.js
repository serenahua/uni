$(document).ready(function() {
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
    $('#chicken_management, #hotpot_management, #expense_management').on('click', 'input[name="type"]', function(e) {
          let cat = $(this).val()
          if (cat == 'income') {
              $('.income_item').removeClass('hide');
              $('.income_item').find('.item_required').addClass('required');
              $('.expense_item').addClass('hide');
              $('.expense_item').find('.item_required').removeClass('required');
          } else if (cat == 'expense') {
              $('.income_item').addClass('hide');
              $('.income_item').find('.item_required').removeClass('required');
              $('.expense_item').removeClass('hide');
              $('.expense_item').find('.item_required').addClass('required');
          }
    })

    // 送出
    $('#chicken_management, #hotpot_management, #expense_management').on('click', '.submit_btn, .continue_btn', function(e) {
          e.preventDefault();

          let next = $(this).hasClass('continue_btn') ? 'reload' : 'home';

          //表顛驗證
          let form = $(this).closest('form');
          var result = checkRequired(form);
          if (!result) {
              return
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

    // 返回
    $('#chicken_management, #hotpot_management, #expense_management').on('click', '.cancel_btn', function(e) {
          e.preventDefault();
          let url = $(this).data('url');
          window.location.href = url;
    })
});