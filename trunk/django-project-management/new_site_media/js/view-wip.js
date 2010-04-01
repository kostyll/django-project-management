
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
		{ name: "pk", mapping: "pk" },
		{ name: "status", mapping: "fields.status" },
		{ name: "heading", mapping: "extras.get_heading" },
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
	sortInfo:{field: 'assignee', direction: "ASC"},
	groupField:'heading',
	autoLoad: true
});

var st_company = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/xhr/get_companies/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"name", mapping: "fields.company_name"}]}),
	autoLoad: true
});

var st_wip_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Active"],[2,"On Hold"]]});

var st_assignee = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/xhr/assignees/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"id", mapping:"pk"},{name:"username", mapping: "fields.username"},{name:"first_name", mapping: "fields.first_name"},{name:"last_name", mapping:"fields.last_name"}]}),
	autoLoad: true
});


var st_heading = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/Headings/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"heading", mapping: "fields.heading"},{name:"company",mapping:"fields.company.company_name"}]}),
	autoLoad: true
});

var st_engineering_day_resource =  new Ext.data.Store({
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk",mapping:"pk"},{name:"resource", mapping:"resource"},{name:"available", mapping:"available"}]})
});

var st_engineering_day_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[0,"Half-day AM"],[1,"Half-day PM"],[2,"Full Day"]]});



/* Form Fields */

wip_item_fields = [
	{ xtype: "combo", fieldLabel: "Heading", hiddenName: "heading", lazyInit: false, store: st_heading, mode: "local", displayField: "heading", valueField: "pk", triggerAction: "all" },
	{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
	{ xtype: "combo", fieldLabel: "Assignee", hiddenName: "assignee", lazyInit: false, store: st_assignee, mode: "local", displayField: "username", valueField: "id", triggerAction: "all" },
	{ xtype: "textarea", fieldLabel: "History", name: "history", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH, readOnly: true  },
	{ xtype: "textarea", fieldLabel: "Update", name: "update", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH  },
	{ xtype: "checkbox", fieldLabel: "Objective", name: "objective" },
	{ xtype: "datefield", fieldLabel: "Deadline", name: "deadline", format: "d/m/Y" },
	{ xtype: "checkbox", fieldLabel: "Complete", name: "complete" },
	{ xtype: "combo", fieldLabel: "Status", hiddenName: "status", lazyInit: false, store: st_wip_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" },
]	

var wip_heading_fields = [
	{ xtype: "textfield", fieldLabel: "Heading", name: "heading" },
	{ xtype: "combo", fieldLabel: "Company", hiddenName: "company", lazyInit: false,  store: st_company, mode: "local", displayField: "name", valueField: "pk", triggerAction: "all" }
]

var get_resources_from_date = function(picker,date_string){

	var day_type = Ext.getCmp("eday_day_type").getValue();
	var chosen_date = new Date(date_string);
	var year = chosen_date.getFullYear();
	var month = chosen_date.getMonth() + 1;
	var day = chosen_date.getDate();
	//Ext.Msg.alert("Hmmmm", "date_string =>" + date_string + ", Year =>" + year + ", Month =>" + month + ", Day =>" + day);
	
	st_engineering_day_resource.proxy = new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/EngineeringDayResources/" + year + "-" + month + "-" + day + "/" + day_type + "/"}),
	st_engineering_day_resource.load();
}

var get_resources_from_day_type = function(){
	
	var day_type = Ext.getCmp("eday_day_type").getValue();
	var date_string = Ext.getCmp("eday_date").getValue();
	var chosen_date = new Date(date_string);
	var year = chosen_date.getFullYear();
	var month = chosen_date.getMonth() + 1;
	var day = chosen_date.getDate();
	
	st_engineering_day_resource.proxy = new Ext.data.HttpProxy({ url: "/WIP/" + wip_report + "/EngineeringDayResources/" + year + "-" + month + "-" + day + "/" + day_type + "/"}),
	st_engineering_day_resource.load();

}

var engineering_day_fields = [
	{ xtype: "datefield", fieldLabel: "Date", format: 'd/m/Y', name: "work_date", listeners: { select: get_resources_from_date }, id: "eday_date" },
	{ xtype: "combo", fieldLabel: "Day Type", hiddenName: "day_type", lazyInit: false, store: st_engineering_day_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all", id: "eday_day_type", listeners: { select: get_resources_from_day_type}, data: '1' },
	{ xtype: "combo", fieldLabel: "Resource", hiddenName: "resource", lazyInit: false, store: st_engineering_day_resource, mode: "local", displayField: "resource", valueField: "pk", triggerAction: "all", height: '200px' }
]
/*
 * Define the form that is used to add/edit WIP items
 */

function user_full_name(val, x, store){
	return store.data.first_name + " " + store.data.last_name;
}

var edit_wip_item = function(b,e){

	var wip_edit_fields = wip_item_fields.slice(1);
	
	var wip_id = grid_wip_items.getSelectionModel().getSelected().get("pk");

	var form_wip_edit = new Ext.form.FormPanel({ url: "/WIP/" + wip_report + "/" + wip_id + "/Update/", bodyStyle: "padding: 15px;", autoScroll: true, items: wip_edit_fields });	

	form_wip_edit.getForm().load({ url: "/WIP/" + wip_report + "/" + wip_id + "/", method: "GET" });	
	var window_edit_wip = new Ext.Window({ width: 620, height: 540, closeAction: "close", autoScroll: true, modal: true, title: "Edit WIP Item", items: [ form_wip_edit ],
		buttons: [ { text: 'Save',
                        handler: function(){
                            form_wip_edit.getForm().submit({
                                            success: function(f,a){
                                            Ext.Msg.alert('Success', 'WIP Item Updated', 
                                            function() { 
                                            	window_edit_wip.hide(); 
                                            	Ext.getCmp("grid_wip_items").store.load();
                                            	Ext.getCmp("work_item_detail").body.update('Please select a Work Item to see more details');
                                          });
									    },  
                                            failure: function(f,a){
                                            	Ext.Msg.alert('Warning', a.result.errormsg);
                                            }
                                        });
                                        }}   
									, { text: 'Close', handler: function(){ window_edit_wip.hide(); } }] });

	window_edit_wip.show();
}

var add_heading = function(){
	var form_add_heading = new Ext.form.FormPanel({ url: "/WIP/" + wip_report + "/Heading/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: wip_heading_fields }); 
	var window_heading = new Ext.Window({autoHeight: true, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a WIP Heading", items: [ form_add_heading ],
			buttons: [{text:'Submit', handler: function(){
					form_add_heading.getForm().submit({
						success: function(f,a){
                                            		Ext.Msg.alert('Success', 'Heading Added');
                                            		window_heading.hide(); 
                                            		st_heading.load();
                                            		},  
                                            		failure: function(f,a){
                                            		Ext.Msg.alert('Warning', a.result.errormsg);
													}
												});
										}}
										, { text: 'Close', handler: function(){ window_heading.hide(); } }] });
	window_heading.show();
}
var add_wip_item = function(){
	var form_add_wip_item = new Ext.form.FormPanel({ url: "/WIP/" + wip_report + "/WIPItem/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: wip_item_fields }); 
	var window_wip_item = new Ext.Window({autoHeight: true, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a WIP Item", items: [ form_add_wip_item ],
			buttons: [{text:'Submit', handler: function(){
					form_add_wip_item.getForm().submit({
						success: function(f,a){
                                            		Ext.Msg.alert('Success', 'WIP Item Added');
                                            		window_wip_item.hide(); 
                                            		Ext.getCmp("grid_wip_items").store.load();
                                            		Ext.getCmp("work_item_detail").body.update('Please select a Work Item to see more details');
                                            		},  
                                            		failure: function(f,a){
                                            		Ext.Msg.alert('Warning', a.result.errormsg);
													}
												});
										}}
										, { text: 'Close', handler: function(){ window_wip_item.hide(); } }] });
	window_wip_item.show();
}


// Complete Work item 
var complete_work_item = function() {
	var work_item_id = grid_wip_items.getSelectionModel().getSelected().get("pk");
	var sm = grid_wip_items.getSelectionModel();
	var sel = sm.getSelected();
	if (sm.hasSelection()){
		Ext.Msg.show({
			title: 'Complete Work Item',
			buttons: Ext.MessageBox.YESNO,
			msg: 'Complete <b>'+sel.data.description+'</b>?',
			closable: false, 
			fn: function(btn){
				if (btn == 'yes'){
						Ext.Ajax.request({
        url: "/WIP/" + wip_report + "/" + work_item_id + "/Complete/",
        method: "POST",
        params: {"pk": work_item_id },
        failure: function (response) {
            Ext.Msg.alert('Error', response.responseText);
        },
        success: function (response) {
            Ext.Msg.alert('Success', sel.data.description + " has been removed");
           Ext.getCmp("grid_wip_items").store.load();
           Ext.getCmp("work_item_detail").body.update('Please select a work item to see more details');
           }
    });
				}
			}
		});
	};
}
 

var add_engineering_day = function(){
	
	var wip_id = grid_wip_items.getSelectionModel().getSelected().get("pk");
	var form_add_engineering_day = new Ext.form.FormPanel({ url: "/WIP/" + wip_report + "/AddEngineeringDay/" + wip_id + "/", bodyStyle: "padding: 15px;", autoScroll: true, items: engineering_day_fields });	
	var window_engineering_day = new Ext.Window({ width: 620, autoHeight: true, closeAction: "close", autoScroll: true, modal: true, title: "Add Engineering Day", items: [ form_add_engineering_day ],
			buttons: [ { text: "Save",
				handler: function(){ 
					form_add_engineering_day.getForm().submit({
						success: function(f,a){
							Ext.Msg.alert('Success', 'Engineering Day Booked',
								function(){
									window_engineering_day.close();
									Ext.getCmp("grid_wip_items").store.load();
                                            				Ext.getCmp("work_item_detail").body.update('Please select a Work Item to see more details');

							});	
						},failure: function(f,a){
							Ext.Msg.alert('Warning', a.result.errormsg);
							}
						});
				}},{ text: "Close", handler: function(){ window_engineering_day.close(); }} ]

	});
	window_engineering_day.show();
}


/*
 * Define the Toolbar buttons for the grid
 */

var btn_add_heading = { iconCls: 'icon-add', text: 'Add Heading', handler: add_heading }
var btn_add_wip_item = { iconCls: 'icon-add', text: 'Add WIP Item', handler: add_wip_item }
var btn_update_wip_item = { iconCls: 'icon-update', text: 'Update WIP Item', handler: edit_wip_item }
var btn_complete_wip_item = { iconCls: 'icon-complete', text: 'Complete WIP Item', handler: complete_work_item }
var btn_add_engineering_day = { iconCls: 'icon-add', text: 'Add Engineering Day', handler: add_engineering_day }


var grid_wip_items = new Ext.grid.GridPanel({
	store: st_wip_items,
	id: "grid_wip_items",
	columns: [
		new Ext.grid.RowNumberer(),
		{ header: "Heading", dataIndex: "heading", sortable: true, hidden: true }, 
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
	tbar: [ btn_add_heading, btn_add_wip_item, btn_update_wip_item, btn_complete_wip_item, btn_add_engineering_day ],
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
	
