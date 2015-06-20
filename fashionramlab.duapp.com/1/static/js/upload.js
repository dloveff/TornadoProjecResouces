$(function(){

    $('.appmsg-thumb-upload').each(function () {

    dropbox = $(this);
    message = $('.message', dropbox);
    
    dropbox.filedrop({
        // The name of the $_FILES entry:
        paramname: 'file',

        maxfiles: 1,
    	maxfilesize: 2, // in mb
        url: '/u',

        uploadFinished:function(i,file,response){
            $.data(file).addClass('done');
            // response is the JSON object that post_file.php returns
        },

    	error: function(err, file) {
            switch(err) {
                case 'BrowserNotSupported':
                    showMessage('浏览器不支持HTML5上传文件!');
                    break;
                case 'TooManyFiles':
                    alert('上传文件数量过多!');
                    break;
                case 'FileTooLarge':
                    alert(file.name+'上传文件太大，超过2MB限额.');
                    break;
                default:
                    break;
            }
        },

        // Called before each upload is started
        beforeEach: function(file){
            if(!file.type.match(/^image\//)){
                alert('只支持图片文件!');

                // Returning false will cause the
                // file to be rejected
                return false;
            }
        },

        uploadStarted:function(i, file, len){
            createImage(file);
        },

        progressUpdated: function(i, file, progress) {
            $.data(file).find('.progress').width(progress);
        }

    });
    
    var template = '<div class="preview">'+
			    '<span class="imageHolder">'+
				'<img />'+
				'<span class="uploaded"></span>'+
			    '</span>'+
			    '<div class="progressHolder">'+
				'<div class="progress"></div>'+
			    '</div>'+
			'</div>'; 
    
    
    function createImage(file){
	var preview = $(template),
	    image = $('img', preview);
    
	var reader = new FileReader();
    
	image.width = 100;
	image.height = 100;
    
	reader.onload = function(e){
	    image.attr('src',e.target.result);
	};
    
	reader.readAsDataURL(file);
    
	message.hide();
	preview.appendTo(dropbox);
    
	$.data(file,preview);
    }

    function showMessage(msg){
        message.html(msg);
    }

    });
});