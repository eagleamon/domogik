/*
 * Build the HTML page with the items of the room
 */
var load = function(idroom){
	new Ajax.Request(BASE_URL+'index.php/lights/room/'+idroom, { 
		onSuccess:function(transport) {
			var _json = transport.responseJSON;
			var nb = 0;
			for (item in _json.root) {
				var name = _json.root[item].name;
				console.log("Name : " + name);
				var color;
				var callback;
				if (Math.floor(nb % 4) == 0) {
					$('images').firstDescendant().insert("<tr></tr>");
				}
				
				if (_json.root[item].value == 1) {
				  	color = IMAGES_DIR+"vert2.png";
					callback = "off(\"" + name + "\")";
				} else {
			    	color = IMAGES_DIR+"red.png";
					callback = "on(\"" + name + "\")";
				}

				var td = "<td><p>" +
					"<span  id='Text"+name+"'>"+_json.root[item].description+"</span>" +
				    "</p>" +
					"<img id='"+name+"' onClick='"+callback+"' class='reflect rheight80 ropacity66' alt='' src='"+color+"' />" +
				"</td>";
				
				$('images').firstDescendant().childElements()[Math.floor(nb / 4)].insert(td);
				 Reflection.add($(name),{ height: 0.8, opacity: 2/3 });
				 nb++;
			}
		}
	})
};

/*
 * Send a request to switch off an item and ask for the item update
 */
var off = function(item) {
	new Ajax.Request(BASE_URL+'index.php/lights/off/' + item, {
		onSuccess: updateItems
	})
}

/*
 * Send a request to switch on an item and ask for the item update
 */
var on = function(item) {
	new Ajax.Request(BASE_URL+'index.php/lights/on/' + item, {
		onSuccess: updateItems
	})
}

/*
 * Update images when getting a JSON message
 */
var updateItems = function(transport) {
          var _json = transport.responseJSON;
		  var color;
		 // $("comment").update("Setting " + _json.name + " with " + _json.value);
		  for (item in _json.root) {
//		  	$("comment").update("Setting " + _json.root[item].name + " with " + _json.root[item].value);
		  if (_json.root[item].value == 1) {
		  	color = "/vert2.png";
		  } else {
		  	color = "/red.png";
		  }
	          $(_json.root[item].name).setAttribute("src",color);
			  $("Text" + _json.root[item].name).update(_json.root[item].description);
			  Reflection.add($(_json.root[item].name),{ height: 0.8, opacity: 2/3 });
		  }
        };
		
var getRemoteContent = function(){
	new Ajax.Request(BASE_URL+'index.php/lights/room/' + $('idroom').getAttribute('value'), {
		onSuccess: updateItems
	})
}
