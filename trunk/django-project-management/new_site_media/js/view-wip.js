
/* Some constants used in forms and grids */
var GRID_HEIGHT = 210
var GRID_WIDTH = 500
var TEXTAREA_WIDTH = 400
var TEXTAREA_HEIGHT = 80 


/*
 * Create work item grid
 */

var st_wip_items = new Ext.data.GroupingStore({
	proxy: new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/?xhr" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
				{ name: "status", mapping: "fields.status" },
				{ name: "modified_date", mapping: "fields.modified_date" },
				{ name: "created_date", mapping: "fields.created_date" },
				{ name: "description", mapping: "fields.description" },
				{ name: "assignee", mapping: "fields.assignee.fields.username" },
				{ name: "deadline", mapping: "fields.deadline" },
				{ name: "complete", mapping: "fields.complete", type: 'bool' },
				{ name: "objective", mapping: "fields.objective", type: 'bool' },
				{ name: "engineering_days", mapping: "fields.engineering_days" },
				{ name: "history", mapping: "fields.history" }
	]}), 
	sortInfo:{field: 'created_date', direction: "ASC"},
	groupField:'assignee',
	autoLoad: true
});


/*
 * Define the form that is used to add/edit WIP items
 */

function user_full_name(val, x, store){
	return store.data.first_name + " " + store.data.last_name;
}

var edit_wip_item = function(b,e){

	var st_assignee = new Ext.data.Store({
		proxy: new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/xhr/assignees/" }),
		reader: new Ext.data.JsonReader({ root: "", fields: [{name:"id", mapping:"pk"},{name:"username", mapping: "fields.username"},{name:"first_name", mapping: "fields.first_name"},{name:"last_name", mapping:"fields.last_name"}]}),
		autoLoad: true
	});

	var st_wip_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Active"],[2,"On Hold"]]});

	wip_form_editor_fields = [
		{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "combo", fieldLabel: "Assignee", hiddenName: "assignee", lazyInit: false, renderer: user_full_name, store: st_assignee, mode: "local", displayField: "username", valueField: "id", triggerAction: "all" },
		{ xtype: "textarea", fieldLabel: "History", name: "history", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, readOnly: true  },
		{ xtype: "textarea", fieldLabel: "Update", name: "update", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH  },
		{ xtype: "checkbox", fieldLabel: "Objective", name: "objective" },
		{ xtype: "datefield", fieldLabel: "Deadline", name: "deadline" },
		{ xtype: "checkbox", fieldLabel: "Complete", name: "complete" },
		{ xtype: "combo", fieldLabel: "Status", hiddenName: "status", lazyInit: false, store: st_wip_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" },
	]	



	var form_wip_edit = new Ext.form.FormPanel({ url: "/WIP/" + wip_report + "/xhr/edit_wip_item/", bodyStyle: "padding: 15px;", autoScroll: true, items: wip_form_editor_fields });	
	
	var win_wip_edit = new Ext.Window({ width: 620, height: 540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit WIP Item", items: [ form_wip_edit ]

	});	
	
	win_wip_edit.show();
}


/*
 * Define the Toolbar buttons for the grid
 */

var btn_add_wip_item = { iconCls: 'icon-add', text: 'Add WIP Item', handler: edit_wip_item }
var btn_update_wip_item = { iconCls: 'icon-update', text: 'Update WIP Item' }
var btn_complete_wip_item = { iconCls: 'icon-complete', text: 'Complete WIP Item' }


var grid_wip_items = new Ext.grid.GridPanel({
	store: st_wip_items,
	columns: [
		new Ext.grid.RowNumberer(),
		{ header: "Status", dataIndex: "status", sortable: true, hidden: true }, 
		{ header: "Modified Date", dataIndex: "modified_date", sortable:true, hidden: true },
		{ header: "Created Date", dataIndex: "created_date", sortable:true, hidden: true },
		{ header: "Description", dataIndex: "description", sortable:true },
		{ header: "Assignee", dataIndex: "assignee", sortable:true },
		{ header: "Deadline", dataIndex: "deadline", sortable:true, hidden: true },
		{ xtype: 'booleancolumn', header: "Complete", dataIndex: "complete", sortable:true, hidden: true,
			trueText: 'Yes', falseText: 'No', editor: { xtype: 'checkbox' } },
		{ xtype: 'booleancolumn', header: "Objective", dataIndex: "objective", sortable:true, 
			trueText: 'Yes', falseText: 'No', editor: { xtype: 'checkbox' } },
		{ header: "Engineering Days", dataIndex: "engineering_days", sortable:true, hidden: true },
	],
	tbar: [ btn_add_wip_item, btn_update_wip_item, btn_complete_wip_item ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	view: new Ext.grid.GroupingView({
            forceFit:true,
            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})'
    }),
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

var wip_item_markup = [
		'<b>Status</b>: {status}<br>',
		'<b>Modified Date</b>: {modified_date}<br>',
		'<b>Created Date</b>: {created_date}<br>',
		'<b>Description</b>: {description}<br>',
		'<b>Assignee</b>: {assignee}<br>',
		'<b>Deadline</b>: {deadline}<br>',
		'<b>Complete</b>: {complete}<br>',
		'<b>Objective</b> {objective}<br>',
		'<b>Engineering Days</b>: {engineering_days}<br>',
		'<b>History</b>: {history}<br>' ];
var wipItemTpl = new Ext.Template(wip_item_markup);


var panel_wip_items = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_wip_items, { id: 'work_item_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a WIP Item to see more details'} ]
});


grid_wip_items.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var wipPanel = Ext.getCmp('work_item_detail');
		wipItemTpl.overwrite(wipPanel.body, r.data);
});


/*
 *
 * Define the tab panels
 *
 */

tab_items = [
	{ xtype: "panel", title: "Agenda", contentEl: "agenda", title: "Agenda" },
	{ xtype: "panel", title: "Objectives", title: "Objectives" },
	{ xtype: "panel", title: "Work In Progress", items: [ panel_wip_items ] }
]

var tabpanel = new Ext.TabPanel({ items: tab_items, bodyStyle: "padding: 15px;", activeTab: 0});
center_panel.items = [ tabpanel ]
	
