/**
 * Created by 锦峰 on 14-1-19.
 */

function create_node(doc, tag, value) {
    var elm = doc.createElement(tag);
    elm.appendChild(doc.createCDATASection(value));
    return elm;
}

function append_cdata_node(doc, parent, tag, value) {
    var elm = doc.createElement(tag);
    elm.appendChild(doc.createCDATASection(value));
    parent.appendChild(elm);
    return elm;
}