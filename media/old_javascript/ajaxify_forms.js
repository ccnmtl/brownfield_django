/* Ajaxify Forms
 * author: schuyler
 * description: This takes forms that submit to a regular location, and 'ajaxifies' 
 *              them, meaning that the method/action is done instead as an XMLHttpRequest()
 * Basic use:
   function myAjaxFormDecorator(ajaxForm_obj) {
      //change ajaxForm_obj.options
      // maybe override ajaxForm_obj.success()  or ajaxForm_obj.failure()
      //
      // connect(ajaxForm_obj,'success',mySuccessFunction); //see MochiKit.Signal
      // ... probably based on ajaxForm.form (class or name)
   }
   addLoadEvent(partial(AjaxFormManager.init,document,myAjaxFormDecorator))

 * The AjaxForm object (what you will decorate/modify):

   AjaxForm.options = {//defaults
	refresh_sections:[],//array of IDs or DOM objects to refresh upon successful form submission
	after_refresh:noop, //function called upon refreshing all refresh_sections
	reset:false,        //after successful form submission should the form be reset?
        accept_xml:true     //send the original request Accept: text/xml for IE support 
	                    //   to take advantage of replaceForm for error reporting

   };
   AjaxForm.success(response) called upon successful form submission.
   AjaxForm.failure(response) called upon successful form failure

   Signals: //see MochiKit.Signal
    'success': when form submission returns successfully
    'failure': when form submission returns an error response
    'afterrefresh': triggered after a refresh OR if there are no refresh sections
        --use this if you want to set content after the DOM is done with any changes

 * Warnings:
   -the AjaxFormManager.init() will be called on all refresh_sections
    (i'm thinking about making this an option) 
    so to renew the ajaxification of any forms within that section
    However, this means that if the form submitted is in this refresh region,
      then AjaxForm.form is a dead reference to the old form that got replaced and
      is no longer on the page/dom.  If the form has an =id= attribute then
      you can do:
         var f = (self.form.id) ? $(self.form.id) : self.form;
      to update your form reference

   -the display page must be valid XHTML

   -IE sux department:
   --If refresh_sections is used, AjaxForm gets a newer version of current URL
       with argument ?cachebuster={randomstring}
       This ensures IE gets a newer version of the current document.

   --Upon request as Accept:text/xml the page should respond with Content-type: text/xml
       so IE includes responseXML

   --Both IE and Safari don't handle named entities like &nbsp; well in this context
       and should be numeric (e.g. &#160;)

   -Firefox sux department:
   -- xmlns="http://www.w3.org/1999/xhtml" MUST be in <html> tag

 * Discussion:
   - This is obviously more bandwidth intensive than returning json data
   - The extra xhtml constraints brought on by browser support issues is annoying
   - However, the nice part is that this keeps templating in templates, and JS
      doesn't have to get involved in how objects are displayed on the page.
 */

AjaxFormManager = {
    ajax_forms:[],
    decorator:noop,
    init:function(parent,decorator) {
	var self = AjaxFormManager;
	if (decorator) {
	    self.decorator = decorator;
	}
	parent = $(parent);
	var forms = parent.getElementsByTagName('form');
	//alert(forms[1].attributes['name'].nodeValue);
	var i = forms.length;
	while (--i >= 0) {
	    var af = new AjaxForm(forms[i], self.ajax_forms, 'AjaxFormManager.ajax_forms');
	    self.decorator(af);
	}
    }
}

function AjaxForm(f, ajax_forms, forms_ref_string) {
    //DEFAULTS
    this.options = {
	refresh_sections:[],//IDs or DOM objects to refresh upon successful form submission
	after_refresh:noop, //function called upon refreshing all refresh_sections
	reset:false,        //reset the form after successful form submission?
	accept_xml:true     //send the original request Accept: text/xml for IE support 
	                    //  to take advantage of replaceForm for error reporting
    };

    this.index = ajax_forms.push(this) -1;

    this.form = f;
    //doing this to accomodate DELETE or PUT methods, which sadly are invalid HTML 4.01
    //but STILL RESTful
    this.method = /*f.method*/getNodeAttribute(f,'method').toUpperCase();
    
    if (this.method == '') {
	this.method = 'GET';
    }
    this.headers = [];
    if (this.method == 'POST') {
	this.headers.push(["Content-Type", 'application/x-www-form-urlencoded']);
    }
    if (this.options.accept_xml) {
	this.headers.push(["Accept", 'text/xml']);
    }

    this.action = f.action;
    //alert(this.action);
    if (this.action == '') {
	this.action = document.location.href;
    }

    this.jsaction = 'javascript:'+forms_ref_string+'['+this.index+'].submit()';
    f.action = this.jsaction;

}

AjaxForm.prototype.submit = function(evt) {
    var self = this;
    var querystr = queryString(self.form);
    var sendContent = (self.method == "GET") ? undefined : querystr;
    var url = (self.method == "GET") ? self.action+'?'+querystr : self.action;

    var def = doXHR(url, {
	'mimeType':'text/xml', //nothing to lose
	'method':self.method,
	'headers':self.headers,
	'sendContent':sendContent
    } );
    def.addCallbacks(bind(self._success,self),bind(self._failure,self));
}

AjaxForm.prototype._success = function(response) {
    var self = this;
    if (self.options.reset) {
	self.form.reset();
    }    
    if (self.options.refresh_sections) {
	var def  = doXHR(location.href+'?cachebuster='+random_string(), {
	    mimeType:'text/xml',
	    headers:{'Accept': 'text/xml'}
	});
	def.addCallback(bind(self.refreshSections,self));
    } else {
	signal(self,'afterrefresh');
    }
    signal(self,'success');
    self.success();
}

/* replaceForm(xmlhttp)
   utility function, which tries to use the body of an error response to 
   replace the form.  
   Requires: 1. return result in text/xml (see options.accept_xml)
             2. the form to have an id="" attribute (same on page as in error response)
   Returns true if replacement was successful

   This is mostly useful for TurboGears/RestResource context, 
     where on errors it returns a new form with specific fielderrors marked.
*/
AjaxForm.prototype.replaceForm= function(xmlhttp) {
    var self = this;

    var formid = self.form.id;
    if (formid) {
	/*
          1. replace form
          2. if new form has action, copy it over
          3. set self.form to the new form
          4. set action on the new form to javascript call
        */

	var newDom = safeGetElement(xmlhttp.responseXML,formid);
	if (newDom) {
	    safeDomReplace(self.form, newDom);
	    newaction = getNodeAttribute(newDom,'action');
	    if (newaction) {
		self.action = newaction;
	    }
	    //setting it through the id is important for IE sux
	    //because newDom still isn't in xml/html namespace, so form.action
	    //doesn't exist
	    self.form = $(formid);

	    self.form.action = self.jsaction;
	    //ignoring any possible change in method for now
	    return true;
	}
    }
    return false;
}

AjaxForm.prototype.success = function(response) {
    alert('submit successful');
}


AjaxForm.prototype._failure = function(err) {
    var self = this;
    signal(self,'failure',arguments);
    self.failure(err);
}

AjaxForm.prototype.failure = function(err) {
    alert('submit failed!');
}


AjaxForm.prototype.refreshSections = function(xmlhttp) {
    var self = this;
    forEach(self.options.refresh_sections, function(sid) {
	swapFromHttp(sid, xmlhttp);

	//(re)-ajaxify any forms in the refreshed area
	AjaxFormManager.init(sid);
    });
    self.options.after_refresh();
    signal(self,'afterrefresh');
}


/***************
  Utility functions: MochiPlus material
***************/


//PYTHONIFY javascript!
function hasattr(obj,key) {
    try {
	return (typeof(obj[key]) != 'undefined');
    } catch(e) {return false;}
}

//PYTHONIFY javascript!
function getattr(obj,key,_default) {
    if (hasattr(obj,key)) {
	if (typeof(obj[key]) == 'unknown') {
	    try{return obj[key]}
	    catch(e){return _default}
	}
	return obj[key];
    }
    if (arguments.length > 2) return  _default;
    throw "AttributeError";
}

/*
  swapFromHttp(myId, xmlhttp)

  Use this in contexts like:
  def = doSimpleXMLHttpRequest('myxmlfile.xml');
  def.addCallback(swapFromHttp, 'myId');
  where $('myId') is the DOM that you want replaced with content
  with the same id="myId" DOM element in the xml request
  caveats:
     IE 6 needs the Content-type: text/xml
     Firefox wants  xmlns="http://www.w3.org/1999/xhtml" in html tag
     IE and Safari don't handle named entities like &nbsp; well in this context
       and should be numeric (e.g. &#160;)

*/
function swapFromHttp(myId, xmlhttp) {
    var resXML=xmlhttp.responseXML;
    var curr=$(myId);
    var newDOM = safeGetElement(resXML,myId);
    var scrollPos=curr.scrollTop; //save scroll position
    
    safeDomReplace(curr,newDOM);

    $(myId).scrollTop = scrollPos;    
    return xmlhttp; //so another deferred can also handle the request;
}

function safeDomReplace(oldDom, newDom) {
    if (/MSIE/.test(navigator.userAgent)) { //IE
	oldDom.outerHTML=newDom.xml;
    } 
    else if (hasattr(newDom,'outerHTML')) { //safari
	oldDom.innerHTML = newDom.innerHTML;
    } else {
	swapDOM(oldDom,newDom);
    }
}

/*  
  safeGetElement(resXML,myId)

  XML objects on responseXML in IE don't have full DOM1,
  so getElementById() doesn't work.  This function does that
  if possible, and for IE it walks the DOM tree looking for your id
*/
function safeGetElement(resXML,myId) {
    var newDOM = null;
    if (typeof(resXML.getElementById) == 'undefined') {
	//IE HACK
	//IE doesn't work because XML DOM isn't as rich as HTML DOM
	var findID = function(node) {
	    if (newDOM) {return null;} //don't waste time after we've found it
	    if (node.nodeType != 1) {
		//document node gets us going
		return (node.nodeType == 9) ? node.childNodes : null; 
	    }
	    if (node.getAttribute('id') == myId) {
		newDOM = node;
		return null;
	    }
	    return node.childNodes;
	};
	nodeWalk(resXML, findID); //walk the html tag
	//curr.outerHTML=newDOM.xml;
    }
    else {
	newDOM=resXML.getElementById(myId);
    }
    return newDOM;

}

//returns a 15-char random string
//utility function to break IE caching
function random_string() {
    var i=16;
    var m = '';
    var asciiChars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    do { 
	m += asciiChars.charAt(Math.floor(62*Math.random()));
    } while(--i);
    return m;
}
