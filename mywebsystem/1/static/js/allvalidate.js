
	/** 
	* 定义验证各种格式类型的正则表达式对象 
	*  
	var Regexs = {  
		email: (/^[0-9a-z][0-9a-z\-\_\.]+@([0-9a-z][0-9a-z\-]*\.)+[a-z]{2,}$/i),//邮箱  
		phone: (/^0[0-9]{2,3}[2-9][0-9]{6,7}$/),//座机手机号码  
		ydphpne: (/^((13[4-9])|(15[012789])|147|182|187|188)[0-9]{8}$/),//移动手机号码  
		allphpne: (/^((13[0-9])|(15[0-9])|(18[0-9]))[0-9]{8}$/),//所有手机号码  
		ltphpne: (/^((13[0-2])|(15[56])|(186)|(145))[0-9]{8}$/),//联通手机号码  
		dxphpne: (/^((133)|(153)|(180)|(189))[0-9]{8}$/),//电信手机号码  
		url: (/^http:\/\/([0-9a-z][0-9a-z\-]*\.)+[a-z]{2,}(:\d+)?\/[0-9a-z%\-_\/\.]+/i),//网址  
		num: (/[^0-9]/),//数字  
		cnum: (/[^0-9a-zA-Z_.-]/),  
		photo: (/\.jpg$|\.jpeg$|\.gif$/i),//图片格式  
		row: (/\n/ig)  
	};  /
	/** 
	* @return 若符合对应的格式，返回true，否则返回false 
	*/  
	function validate_email(str){
		email= /^[0-9a-z][0-9a-z\-\_\.]+@([0-9a-z][0-9a-z\-]*\.)+[a-z]{2,}$/i ;   //邮箱  
		return emai.test(str);   //成功返回true
	}
	function validate_phone(str){
	   phone = /^0[0-9]{2,3}[2-9][0-9]{6,7}$/; //座机和手机
	   return phone.test(str); //成功返回true
	}
	function validate_allphpne(str){
		allphpne = /^((13[0-9])|(15[0-9])|(18[0-9]))[0-9]{8}$/; //所有手机号码
		return allphpne.test(str);//成功返回true
	}
	function validate_ydphpne(str){
	   ydphpne = /^((13[4-9])|(15[012789])|147|182|187|188)[0-9]{8}$/; //移动手机号码
	   return ydphpne.test(str); //成功返回true
	}

	function validate_ltphpne(str){
		ltphpne = /^((13[0-2])|(15[56])|(186)|(145))[0-9]{8}$/; //联通手机号码
		return ltphpne.test(str);//成功返回true
	}
	function validate_dxphpne(str){
		dxphpne = /^((133)|(153)|(180)|(189))[0-9]{8}$; //电信手机号码
		return dxphpne.test(str);//成功返回true
	}
	function validate_url(str){
		url = /^http:\/\/([0-9a-z][0-9a-z\-]*\.)+[a-z]{2,}(:\d+)?\/[0-9a-z%\-_\/\.]+/i; //网址
		return url.test(url);//成功返回true
	}
	function validate_num(str){
		num = /[^0-9]/;//数字
		return num.test(str);
	}
	function validate_cnum(str){
		cnum = /[^0-9a-zA-Z_.-]/; //数字或字母
		return cnum.test(str);
	}
	function validate_image(str){
		image = /\.jpg$|\.jpeg$|\.gif$/i;  //图片格式
		return image.test(str);
	}

	function checkGroupName() {   //验证非法字符
		var reg = /^([0-9a-zA-Z])|([\u4e00-\u9fa5])$/;
		var str = $('#pass').val();
		if (!reg.test(str)) {
			$('#pass').val("");   //清空密码输入框   <input class="input-large span10" name="password" id="pass" type="password" onkeyup="checkGroupName()"/>
			console.log("对不起，你输入的内容含有非法字符！");
		}
	}



