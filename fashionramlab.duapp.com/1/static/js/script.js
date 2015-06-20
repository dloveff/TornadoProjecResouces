

function console_recv_patternShow(id){
	$.confirm({
			'title'		: '温馨提示',
			'message'	: '<h5>确认删除？</h5>',
			'buttons'	: {
				'确认'	: {
					'class'	: 'blue',
					'action': function(){
						deletePattern(id);
						allconsole_recv();
					}
				},
				'取消'	: {
					'class'	: 'gray',
					'action': function(){}	
				}
			}
		});
	
	
}
