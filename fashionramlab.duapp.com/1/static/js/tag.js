/**
 * Created by TsukiHiBoshi on 14-1-6.
 */

/*
 *  /mptags/(mpid) - GET
 *  获得一个xml文本：
 *  <tags>
 *      <tag name="一层标签" order="0">
 *          <children>
 *              <tag name="二层标签" order="0"/>
 *              <tag name="二二标签" order="1"/>
 *          </children>
 *      </tag>
 *      <tag name="第二个标签" order="0"/>
 *  </tag>
 *
 *  要求输出成 json：
 *
 *  {
 *      "一层标签": { "value": "/一层标签/", "order": 0, children: {"二层标签":{ "value": "/一层标签/二层标签/", "order": 0 },"二二标签":{ "value": "/一层标签/二二标签/", "order": 1} ],
 *      "第二个标签": {"value": "/第二个标签/" }
 *  }
 */
function get_tag_list() {
  var id=$("#mpid").val();
  $.ajax({
		   type:'GET',
		   url: '/mptags/'+id,
		   success:function(date){
           $("#tagList option").remove();
           for(var o in date){
                var pa = $('<option/>');
					pa.val(date[o].value);
					pa.text(o);
				    $(".tagList").append(pa);
               for(var y in date[o].children){
                   var pa = $('<option/>');
					pa.val(date[o].children[y].value);
					pa.text("--"+y);
				    $(".tagList").append(pa);
               }
              }
		    }

		   });

}
function changeForm(){
   var mun=$(".tagList").val();
   if(mun=="全部"){
       findconsole_module_cms();
   }else{
           findtag(mun);
    }

}
/*
 *  /mptags/(mpid) - POST
 *
 *  要求输入 json：
 *
 *
 *  {
 *      "一层标签": { "value": "/一层标签/", "order": 0, children: {"二层标签":{ "value": "/一层标签/二层标签/", "order": 0 },"二二标签":{ "value": "/一层标签/二二标签/", "order": 1} ],
 *      "第二个标签": {"value": "/第二个标签/" }
 *  }
 *
 *  把上述输入转换成下列xml 提交
 *  <tags>
 *      <tag name="一层标签" order="0">
 *          <children>
 *              <tag name="二层标签" order="0"/>
 *              <tag name="二二标签" order="1"/>
 *          </children>
 *      </tag>
 *      <tag name="第二个标签" order="0"/>
 *  </tag>
 */
function set_tag_list(mpid, data) {
       var id=$("#mpid").val();
         $.ajax({
			    type: 'POST',
			    url: '/mptags/'+id,
               dataType: 'json',
			   data:pattern,
			   success: function(date) {


			   },error: function(XMLHttpRequest, textStatus, errorThrown) {

                    }

			});

}