(window.webpackJsonp=window.webpackJsonp||[]).push([[196],{824:function(t,e,o){"use strict";o.r(e),o.d(e,"default",(function(){return l}));var n=o(5),a=o(9),c=o(7),i=o(8),r=o(2),u=o(1);function s(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}();return function(){var o,n=Object(r.a)(t);if(e){var a=Object(r.a)(this).constructor;o=Reflect.construct(n,arguments,a)}else o=n.apply(this,arguments);return Object(i.a)(this,o)}}var l=function(t){Object(c.a)(o,t);var e=s(o);function o(t){var a;return Object(n.a)(this,o),(a=e.call(this,t)).props.isEmbeded||(a.cacheChildrenEl({input:a.props.input}),a.setup()),a}return Object(a.a)(o,[{key:"setup",value:function(t){this.$input.classList.add("disabled"),this.$input.disabled=!0}},{key:"autoLocate",value:function(){var t=this;return this.setState({loading:!0}),this.fetch().then((function(e){t.setState({disabled:!1,loading:!1,coordinates:{lat:e.coords.latitude,lng:e.coords.longitude}})})).catch((function(){t.setState({loading:!1})}))}},{key:"fetch",value:function(){var t=this;return new Promise((function(e,o){navigator.geolocation?(t.setState({autoLocateError:!1}),navigator.geolocation.getCurrentPosition((function(n){if(t.props.isRangeBlocked())return t.props.parent.props.onConflict(),void o();e(n)}),(function(){t.setState({autoLocateError:!0}),o()}),{timeout:1e4,maximumAge:6e4,enableHighAccuracy:!0})):t.setState({autoLocateError:!0})}))}},{key:"clear",value:function(){this.setState({disabled:!0,coordinates:{lat:"",lng:""}})}},{key:"render",value:function(t,e){"disabled"!==t&&"coordinates"!==t&&"autoLocateError"!==t&&"loading"!==t||this.props.update(Object(u.a)({},t,e)),"coordinates"===t&&(this.$input.value=e.lat&&e.lng?"".concat(e.lat.toFixed(6),", ").concat(e.lng.toFixed(6)):""),"disabled"===t&&(this.$input.classList.toggle("disabled",e),this.$clear.classList.toggle("hidden",e))}}]),o}(o(11).a);Object(u.a)(l,"childrenEl",{button:".GeoLocationSelector-autoLocateButton",clear:".GeoLocationSelector-iconClose"}),Object(u.a)(l,"events",{"click .GeoLocationSelector-iconClose":"clear","click .GeoLocationSelector-autoLocateButton":"autoLocate"})}}]);