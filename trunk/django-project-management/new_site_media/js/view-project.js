
/* Some constants used in forms and grids */
var GRID_HEIGHT = 210
var GRID_WIDTH = 500
var TEXTAREA_WIDTH = 400
var TEXTAREA_HEIGHT = 80 

/* 
 * Some reusable functions
 *
 */


var st_users = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/xhr/get_users" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "fields.username"}]}),
	autoLoad: true
});


 /* 
 *
 * DELIVERABLES!!!!
 *
 * */

var deliverable_fields = [
		{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Acceptance Criteria", name: "acceptance_criteria", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textfield", fieldLabel: "Deliverable Tester", name: "deliverable_tester" },
		{ xtype: "textarea", fieldLabel: "Method", name: "testing_method", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Expected Result", name: "expected_result", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textfield", fieldLabel: "RPO", name: "rpo" },
		{ xtype: "textfield", fieldLabel: "RTO", name: "rto" } ]

// Add a Deliverable
var add_deliverable = function(b,e){
	
	var form_add_deliverable = new Ext.form.FormPanel({ url: "/Deliverables/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: deliverable_fields });
										
	var window_deliverable = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Deliverable", items: [ form_add_deliverable ],
							buttons: [	{ 	text:'Submit', 
											handler: function(){
												form_add_deliverable.getForm().submit({
													success: function(f,a){
                                            		Ext.Msg.alert('Success', 'Deliverable Added');
                                            		},  
                                            		failure: function(f,a){
                                            		Ext.Msg.alert('Warning', 'An Error occured');
													}
												});
										}}
										, { text: 'Close', handler: function(){ window_deliverable.hide(); } }] });
	tabpanel.activate(1);
	window_deliverable.show();
}

// Edit Deliverable
var edit_deliverable = function(b,e){

	var	deliverable_id = grid_deliverables.getSelectionModel().getSelected().get("pk");
	var form_deliverable_edit = new Ext.form.FormPanel({url: "/Deliverables/" + project_number + "/" + deliverable_id + "/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: deliverable_fields });
	form_deliverable_edit.getForm().load({ url: "/Deliverables/" + project_number + "/" + deliverable_id + "/", method: "GET" });
	
	var window_deliverable = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit a Deliverable", items: [ form_deliverable_edit ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         form_deliverable_edit.getForm().submit({
                                            success: function(f,a){
                                            Ext.Msg.alert('Success', 'Deliverable Updated', 
                                            function() { 
                                            	window_deliverable.hide(); 
                                            	Ext.getCmp("d_grid").store.load();
                                            	Ext.getCmp("deliverable_detail").body.update('Please select a deliverable to see more details');
                                            	});
									    },  
                                            failure: function(f,a){
                                            Ext.Msg.alert('Warning', 'An Error occured');
                                            }
                                        });
                                        }}   
									, { text: 'Close', handler: function(){ window_deliverable.hide(); } }] });
	window_deliverable.show();
}

// Delete Deliverable
var delete_deliverable = function(){
	Ext.Msg.alert("Warning", "Placeholder... code to be written here");
}
 
// Show Deliverables... 
var st_deliverable = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Deliverables/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [	{name:"description", mapping: "fields.description"},
															{name:"pk", mapping: "pk"},
															{name:"acceptance_criteria", mapping: "fields.acceptance_criteria"},
															{name:"deliverable_tester",mapping:"fields.deliverable_tester"},
															{name:"testing_method", mapping: "fields.testing_method"},
															{name:"expected_result", mapping: "fields.expected_result"},
															{name:"rpo", mapping: "fields.rpo"},
															{name:"rto", mapping: "fields.rto"},
															{name:"created_date", mapping: "fields.created_date"},
															{name:"modified_date", mapping: "fields.modified_date"} ]}),
	autoLoad: true
});

var btn_update_deliverable = { iconCls: 'icon-update', text: 'Update Deliverable', handler: edit_deliverable }
var btn_delete_deliverable = { iconCls: 'icon-complete', text: 'Delete Deliverable', handler: delete_deliverable }

var grid_deliverables = new Ext.grid.GridPanel({
        store: st_deliverable,
        columns: [
            {header: "Description", dataIndex: 'description', sortable: true},
            {header: "Acceptance Criteria", dataIndex: 'acceptance_criteria', sortable: true},
            {header: "Tester", dataIndex: 'deliverable_tester', sortable: true},
            {header: "Method", dataIndex: 'testing_method', sortable: true, hidden: true},
            {header: "Expected Result", dataIndex: 'expected_result', sortable: true, hidden: true},
            {header: "RTO", dataIndex: 'rto', sortable: true, hidden: true },
            {header: "RPO", dataIndex: 'rpo', sortable: true, hidden: true },
            {header: "Created Date", dataIndex: 'created_date', sortable: true, hidden: true },
            {header: "Modified Date", dataIndex: 'modified_date', sortable: true, hidden: true } ],
        tbar: [ btn_update_deliverable, btn_delete_deliverable ],
		sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
		viewConfig: { forceFit: true },
        height: GRID_HEIGHT,
        id:'d_grid',
		width: GRID_WIDTH,
		split: true,
		region: 'west'
});

var markup_deliverables = [
	'<table class="project_table">',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>Deliverable Tester</th> <td>{deliverable_tester}</td></tr>',
	'<tr><th>Acceptance Criteria</th> <td>{acceptance_criteria}</td></tr>',
	'<tr><th>Method</th> <td>{testing_method}</td></tr>',
	'<tr><th>Expected Result</th> <td>{expected_result}</td></tr>',
	'<tr><th>RPO</th> <td>{rpo}</td></tr>',
	'<tr><th>RTO</th> <td>{rto}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var template_deliverables = new Ext.Template(markup_deliverables);

var panel_deliverables = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_deliverables, { id: 'deliverable_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a deliverable to see more details'} ]
});

grid_deliverables.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var detailPanel = Ext.getCmp('deliverable_detail');
		template_deliverables.overwrite(detailPanel.body, r.data);
});

/*
 *
 * RISKS!!!
 *
 * */
probability_list = ["", "Very Unlikely", "Unlikely", "Possible", "Likely"]
impact_list = ["", "Low Impact", "Some Impact", "High Impact", "Critical"]
var probability_tip = new Ext.ux.SliderTip({ getText: function(slider){ return String.format('<b>{0}</b>', probability_list[slider.getValue()]); } }); 
var impact_tip = new Ext.ux.SliderTip({ getText: function(slider){ return String.format('<b>{0}</b>', impact_list[slider.getValue()]); } }); 
var st_counter = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Prevention"],[2,"Acceptance"],[3,"Transfer"],[4,"Reduction"],[5,"Contingency"]]});
var st_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Closed"],[2,"Reducing"],[3,"Increasing"],[4,"No Change"]]});

var risk_fields = [
	{ xtype: "textfield", fieldLabel: "Risk Number", name: "risk_number" },
	{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
	{ xtype: "combo", fieldLabel: "Owner", name: "owner", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all" },
	{ xtype: "slider", minValue: 1, maxValue: 4, plugins: probability_tip, fieldLabel: "Probability", name: "probability" },
	{ xtype: "slider", minValue: 1, maxValue: 4, plugins: impact_tip, fieldLabel: "Impact", name: "impact" },
	{ xtype: "textfield", fieldLabel: "Rating", name: "rating", readOnly: true },
	{ xtype: "combo", displayField: "d", valueField: "id", mode: "local", store: st_counter, fieldLabel: "Counter Measure", name: "counter_measure", triggerAction: "all" },
	{ xtype: "combo", displayField: "d", valueField: "id", mode: "local", store: st_status, fieldLabel: "Status", name: "status", triggerAction: "all" }]

var add_risk = function(b,e){

	
	var form_risk_add = new Ext.form.FormPanel({ url: "/Risks/" + project_number + "/Add/", bodyStyle: "padding: 15px;", autoScroll: true, items: risk_fields});

	var window_risks = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Risk", items: [ form_risk_add ],
							buttons: [{ text:'Submit', disabled:true }, { text: 'Close', handler: function(){ window_risks.hide(); } }] });
	project_menu.hide();
	tabpanel.activate(2);
	window_risks.show();
}

var edit_risk = function(b,e){
	var	risk_id = grid_risks.getSelectionModel().getSelected().get("pk");
	var form_risk_edit = new Ext.form.FormPanel({ url: "/Risks/" + project_number + "/" + risk_id + "/Edit/", bodyStyle: "padding: 15px;", autoScroll: true, items: risk_fields});
	form_risk_edit.getForm().load({ url: "/Risks/" + project_number + "/" + risk_id + "/", method: "GET" });
	var window_risks = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Risk", items: [ form_risk_edit ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         form_risk_edit.getForm().submit({
                                            success: function(f,a){
                                            Ext.Msg.alert('Success', 'Risk Updated', function() { window_risks.hide(); window.location.reload();});
									    },  
                                            failure: function(f,a){
                                            Ext.Msg.alert('Warning', 'An Error occured');
                                            }
                                        });
                                        }}   
									, { text: 'Close', handler: function(){ window_risks.hide(); } }] });
	window_risks.show();

}


// Delete Risk
var delete_risk = function(){
	Ext.Msg.alert("Warning", "Placeholder... code to be written here");
}


var st_risks = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Risks/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [   
		{name:"pk", mapping: "pk"},
		{ name: "risk_number", mapping: "fields.risk_number" },
		{ name: "created_date", mapping: "fields.created_date" },	
		{ name: "modified_date", mapping: "fields.modified_date" },	
		{ name: "description", mapping: "fields.description" },	
		{ name: "owner", mapping: "fields.owner.fields.username" },	
		{ name: "probability", mapping: "fields.probability" },	
		{ name: "impact", mapping: "fields.impact" },	
		{ name: "rating", mapping: "fields.rating" },	
		{ name: "counter_measure", mapping: "fields.counter_measure" },	
		{ name: "status", mapping: "fields.status" }	]	}),
	autoLoad: true
});

var btn_update_risk = { iconCls: 'icon-update', text: 'Update Risk', handler: edit_risk }
var btn_delete_risk = { iconCls: 'icon-complete', text: 'Delete Risk', handler: delete_risk }

var grid_risks = new Ext.grid.GridPanel({
        store: st_risks,
        columns: [
            {header: "Risk Number", dataIndex: 'risk_number'},
            {header: "Description", dataIndex: 'description'},
            {header: "Probability", dataIndex: 'probability'},
            {header: "Impact", dataIndex: 'impact'},
	    {header: "Rating", dataIndex: 'rating'} ],
		sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
		viewConfig: { forceFit: true },
        tbar: [ btn_update_risk, btn_delete_risk ],
        height: GRID_HEIGHT,
		width: GRID_WIDTH,
		split: true,
		region: 'west'
});

var riskMarkup = [
	'<table class="project_table">',
	'<tr><th>Risk Number</th> <td>{risk_number}</td></tr>',
	'<tr><th>Description</th> <td>{description}</td></tr>',
	'<tr><th>Owner</th> <td>{owner}</td></tr>',
	'<tr><th>Probability</th> <td>{probability}</td></tr>',
	'<tr><th>Impact</th> <td>{impact}</td></tr>',
	'<tr><th>Rating</th> <td>{rating}</td></tr>',
	'<tr><th>Counter Measure</th> <td>{counter_measure}</td></tr>',
	'<tr><th>Status</th> <td>{status}</td></tr>',
	'<tr><th>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var riskTpl = new Ext.Template(riskMarkup);

var risk_panel = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_risks, { id: 'risk_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a Risk to see more details'} ]
});

grid_risks.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var riskPanel = Ext.getCmp('risk_detail');
		riskTpl.overwrite(riskPanel.body, r.data);
});

/*
 *
 * Create the WBS Grid 
 *
 * */

var st_wbs = new Ext.data.GroupingStore({
	proxy: new Ext.data.HttpProxy({ url: "/WBS/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "created_date", mapping: "fields.created_date" },
		{ name: "modified_date", mapping: "fields.modified_date" },
		{ name: "skill_set", mapping: "fields.skill_set.fields.skill" },
		{ name: "project_phase", mapping: "fields.project_phase.fields.phase" },
		{ name: "author", mapping: "fields.author.fields.username" },
		{ name: "title", mapping: "fields.title" },
		{ name: "description", mapping: "fields.description" },
		{ name: "number_days", mapping: "fields.number_days" },
		{ name: "owner", mapping: "fields.owner.fields.username" },
		{ name: "percent_complete", mapping: "fields.percent_complete" },
		{ name: "start_date", mapping: "fields.start_date" },
		{ name: "finish_date", mapping: "fields.finish_date" },
		{ name: "wbs_number", mapping: "fields.wbs_number" },
		{ name: "cost", mapping: "fields.cost" },
		{ name: "history", mapping: "fields.history" },
		{ name: "engineering_days", mapping: "fields.engineering_days" } ]}),
	autoLoad: true,
	groupField: 'project_phase',
	sortInfo:{field: 'wbs_number', direction: "ASC"}
});


var btn_update_wbs = { iconCls: 'icon-update', text: 'Update Work Item', handler: null }
var btn_delete_wbs = { iconCls: 'icon-complete', text: 'Delete Work Item', handler: null }

var grid_wbs = new Ext.grid.GridPanel({
        store: st_wbs,
        columns: [
            {header: "WBS Number", dataIndex: 'wbs_number'},
            {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true },
            {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true },
            {header: "Skill Set", dataIndex: 'skill_set', hidden: true, sortable: true },
            {header: "Phase", dataIndex: 'project_phase'},
            {header: "Author", dataIndex: 'author', hidden: true, sortable: true },
            {header: "Title", dataIndex: 'title', sortable: true },
            {header: "Description", dataIndex: 'description', hidden: true },
            {header: "Number of Days", dataIndex: 'number_days', hidden: true, sortable: true },
            {header: "Owner", dataIndex: 'owner', hidden: true, sortable: true },
            {header: "Percent Complete", dataIndex: 'percent_complete', sortable: true },
            {header: "Start Date", dataIndex: 'start_date', hidden: true, sortable: true },
            {header: "Finish Date", dataIndex: 'finish_date', hidden: true, sortable: true },
            {header: "Cost", dataIndex: 'cost'}
		],
        tbar: [ btn_update_wbs, btn_delete_wbs ],
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

var markup_wbs = [
	'<table class="project_table">',
	'<tr><td>WBS Number</th> <td>{wbs_number}</td></tr>',
	'<tr><td>Skillset</th> <td>{skill_set}</td></tr>',
	'<tr><td>Phase</th> <td>{phase}</td></tr>',
	'<tr><td>Title</th> <td>{title}</td></tr>',
	'<tr><td>Description</th> <td>{description}</td></tr>',
	'<tr><td>Author</th> <td>{author}</td></tr>',
	'<tr><td>Depends Upon</th> <td>{depends}</td></tr>',
	'<tr><td>Number of Days</th> <td>{number_days}</td></tr>',
	'<tr><td>Owner</th> <td>{owner}</td></tr>',
	'<tr><td>Cost</th> <td>{cost}</td></tr>',
	'<tr><td>Percent Complete</th> <td>{percent_complete}</td></tr>',
	'<tr><td>Start Date</th> <td>{start_date}</td></tr>',
	'<tr><td>Finish Date</th> <td>{finish_date}</td></tr>',
	'<tr><td>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><td>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_wbs = new Ext.Template(markup_wbs);

var panel_wbs = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_wbs, { id: 'wbs_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select a Work Item to see more details'} ]
});

grid_wbs.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_wbs = Ext.getCmp('wbs_detail');
		tpl_wbs.overwrite(panel_wbs.body, r.data);
});


/*
 *
 * Create the Issues Grid
 *
 */
var st_issue_type = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Request For Change"],[2,"Off Specifications"],[3,"Concern"],[4,"Question"]]});
var st_issue_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"Open"],[2,"In Progress"],[3,"Completed"],[4,"Closed"]]});
var st_issue_priority = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[1,"1"],[2,"2"],[3,"3"],[4,"4"],[5,"5"]]});
var issue_fields = [
	{ xtype: "textarea", fieldLabel: "Description", name: "description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
	{ xtype: "combo", fieldLabel: "Owner", name: "owner", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all" },
	{ xtype: "combo", fieldLabel: "Author", name: "author", lazyInit: false, store: st_users, mode: "local", displayField: "username", valueField: "pk", triggerAction: "all" },
	{ xtype: "combo", fieldLabel: "Type", name: "type", lazyInit: false, store: st_issue_type, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" },
	{ xtype: "combo", fieldLabel: "Status", name: "status", lazyInit: false, store: st_issue_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" },
	{ xtype: "combo", fieldLabel: "Priority", name: "priority", lazyInit: false, store: st_issue_priority, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" }, 
	{ xtype: "textfield", fieldLabel: "Related RFC", name: "related_rfc" },
	{ xtype: "textfield", fieldLabel: "Related Helpdesk", name: "related_helpdesk" }]

var add_issue = function(b,e){
	var form_add_issue = new Ext.form.FormPanel({ url: "/Issues/" + project_url + "/AddIssue/", bodyStyle: "padding: 15px;", autoScroll: true, items: issue_fields});
	var window_issues = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Add a Issue", items: [ form_add_issue ],
							buttons: [	{ 	text:'Submit', 
											handler: function(){
												form_add_issue.getForm().submit({
													success: function(f,a){
                                            		Ext.Msg.alert('Success', 'Issue Added');
                                            		},  
                                            		failure: function(f,a){
                                            		Ext.Msg.alert('Warning', 'An Error occured');
													}
												});
										}}
										, { text: 'Close', handler: function(){ window_issue.hide(); } }] });
	project_menu.hide();
	tabpanel.activate(4);
	window_issues.show();
}

var st_issues = new Ext.data.GroupingStore({
	proxy: new Ext.data.HttpProxy({ url: "/Issues/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "created_date", mapping: "fields.created_date" },
		{ name: "modified_date", mapping: "fields.modified_date" },
		{ name: "description", mapping: "fields.description" },
		{ name: "owner", mapping: "fields.owner.fields.username" },
		{ name: "author", mapping: "fields.author.fields.username" },
		{ name: "type", mapping: "fields.type" },
		{ name: "status", mapping: "fields.status" },
		{ name: "priority", mapping: "fields.priority" },
		{ name: "related_rfc", mapping: "fields.related_rfc" },
		{ name: "related_helpdesk", mapping: "fields.related_helpdesk" } ]}),
	autoLoad: true,
    groupField: 'type',
	sortInfo:{field: 'description', direction: "ASC"}
});

var btn_update_issues = { iconCls: 'icon-update', text: 'Update Issue', handler: edit_deliverable }
var btn_delete_issues = { iconCls: 'icon-complete', text: 'Delete Issue', handler: edit_deliverable }

var grid_issues = new Ext.grid.GridPanel({
	store: st_issues,
	columns: [
            {header: "Description", dataIndex: 'description'},
            {header: "Owner", dataIndex: 'owner', sortable: true},
            {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true },
            {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true },
            {header: "Author", dataIndex: 'author', hidden: true, sortable: true },
            {header: "Status", dataIndex: 'status', sortable: true },
            {header: "Type", dataIndex: 'type', sortable: true },
            {header: "Priority", dataIndex: 'priority' },
            {header: "Related RFC", dataIndex: 'related_rfc', hidden: true, sortable: true},
            {header: "Related Helpdesk", dataIndex: 'related_helpdesk', hidden: true, sortable: true}
	],
    tbar: [ btn_update_issues, btn_delete_issues ],
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

var markup_issues = [
	'<table class="project_table">',
	'<tr><td>Owner</th> <td>{owner}</td></tr>',
	'<tr><td>Description</th> <td>{description}</td></tr>',
	'<tr><td>Author</th> <td>{author}</td></tr>',
	'<tr><td>Type</th> <td>{type}</td></tr>',
	'<tr><td>Status</th> <td>{status}</td></tr>',
	'<tr><td>Priority</th> <td>{priority}</td></tr>',
	'<tr><td>Related RFC</th> <td>{related_rfc}</td></tr>',
	'<tr><td>Related Helpdesk</th> <td>{related_helpdesk}</td></tr>',
	'<tr><td>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><td>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_issues = new Ext.Template(markup_issues);

var panel_issues = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_issues, { id: 'issues_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Issue to see more details'} ]
});

grid_issues.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_issues = Ext.getCmp('issues_detail');
		tpl_issues.overwrite(panel_issues.body, r.data);
});


/*
 *
 * Create the Lessons Learnt Grid
 *
 */

var st_lessons = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Lessons/" + project_number + "/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "author", mapping: "fields.author" },
		{ name: "description", mapping: "fields.description" },
		{ name: "created_date", mapping: "fields.created_date" },
		{ name: "modified_date", mapping: "fields.modified_date" },
		{ name: "publish_to_client", mapping: "fields.publish_to_client" } ]}),
	autoLoad: true
});

var btn_update_lesson = { iconCls: 'icon-update', text: 'Update Lesson', handler: edit_deliverable }
var btn_delete_lesson = { iconCls: 'icon-complete', text: 'Delete Lesson', handler: edit_deliverable }

var grid_lessons = new Ext.grid.GridPanel({
	store: st_lessons,
	columns: [
            {header: "Description", dataIndex: 'description'},
            {header: "Author", dataIndex: 'Author', hidden: true, sortable: true },
            {header: "Created Date", dataIndex: 'created_date', hidden: true, sortable: true },
            {header: "Modified Date", dataIndex: 'modified_date', hidden: true, sortable: true },
            {header: "Publish To Client", dataIndex: 'publish_to_client', sortable: true }
	],
    tbar: [ btn_update_lesson, btn_delete_lesson ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

var markup_lessons = [
	'<table class="project_table">',
	'<tr><td>Description</th> <td>{description}</td></tr>',
	'<tr><td>Author</th> <td>{author}</td></tr>',
	'<tr><td>Publish To Client</th> <td>{publish_to_client}</td></tr>',
	'<tr><td>Created Date</th> <td>{created_date}</td></tr>',
	'<tr><td>Modified Date</th> <td>{modified_date}</td></tr>', '</table>' ];
var tpl_lessons = new Ext.Template(markup_lessons);

var panel_lessons = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_lessons, { id: 'lessons_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Lesson to see more details'} ]
});

grid_lessons.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_lessons = Ext.getCmp('lessons_detail');
		tpl_lessons.overwrite(panel_lessons.body, r.data);
});


/*
 *
 * Create the Project Report Grid
 *
 */

var st_report = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Projects/" + project_number + "/Updates/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{ name: "author", mapping: "fields.author.fields.username" },
		{ name: "type", mapping: "fields.type" },
		{ name: "created_date", mapping: "fields.created_date" },
		{ name: "modified_date", mapping: "fields.modified_date" },
		{ name: "summary", mapping: "fields.summary" } ]}),
	autoLoad: true
});

var btn_update_report = { iconCls: 'icon-update', text: 'Update Report', handler: edit_deliverable }
var btn_delete_report = { iconCls: 'icon-complete', text: 'Delete Report', handler: edit_deliverable }

var grid_report = new Ext.grid.GridPanel({
	store: st_report,
	columns: [
            {header: "Summary", dataIndex: 'summary'},
            {header: "Author", dataIndex: 'author', sortable: true},
            {header: "Created_date", dataIndex: 'created_date', hidden: true, sortable: true },
            {header: "Type", dataIndex: 'type', hidden: true, sortable: true },
            {header: "Modified Date", dataIndex: 'modified_date', sortable: true, hidden: true}
	],
    tbar: [ btn_update_report ],
	sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
	viewConfig: { forceFit: true },
    height: GRID_HEIGHT,
	width: GRID_WIDTH,
	split: true,
	region: 'west'
});

var markup_report = [
	'<table class="project_table">',
	'<tr><th>Author</th><td>{author}</td></tr>',
	'<tr><th>Summary</th><td>{summary}</td></tr>',
	'<tr><th>Type</th><td>{type}</td></tr>',
	'<tr><th>Created Date</th><td>{created_date}</td></tr>',
	'<tr><th>Modified Date</th><td>{modified_date}</td></tr>', '</table>' ];
var tpl_report = new Ext.Template(markup_report);

var panel_report = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_report, { id: 'report_detail', bodyStyle: { background: '#ffffff', padding: '7px' }, region: 'center', html: 'Please select an Update to see more details'} ]
});

grid_report.getSelectionModel().on('rowselect', function(sm, rowIdx, r) {
		var panel_report = Ext.getCmp('report_detail');
		tpl_report.overwrite(panel_report.body, r.data);
});



/* 
 *
 * Edit the Project Initation data 
 *
 * */
var edit_project_initiation = function(b,e){
	var st_company = new Ext.data.Store({
		proxy: new Ext.data.HttpProxy({ url: "/xhr/get_companies" }),
		reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"name", mapping: "fields.company_name"}]}),
		autoLoad: true
	});

	var st_project_status = new Ext.data.ArrayStore({fields: ["id", "d"], data: [[0,"Proposed"],[1,"Draft"],[2,"Active"],[3,"On Hold"],[4,"Completed"],[5,"Archived"]]});


	var project_initiation_fields = [
		{ xtype: "textfield", fieldLabel: "Project Name", name: "project_name" },
		{ xtype: "textfield", fieldLabel: "Project Number", name: "project_number" },
		{ xtype: "combo", fieldLabel: "Project Status", hiddenName: "project_status", lazyInit: false,  store: st_project_status, mode: "local", displayField: "d", valueField: "id", triggerAction: "all" },
		{ xtype: "combo", fieldLabel: "Company", hiddenName: "company", lazyInit: false,  store: st_company, mode: "local", displayField: "name", valueField: "pk", triggerAction: "all" },
		{ xtype: "textfield", fieldLabel: "Project Manager", name: "project_manager" },

		{ xtype: 'itemselector', name: "team_managers_placeholder", hiddenName: 'team_managers_placeholder', fieldLabel: 'Team Managers',
	        imagePath: '/site_media/js/extjs/examples/ux/images/',
			allowBlank: false,
            multiselects: [{
				legend: "Available People",
				scroll: true,
                width: 200,
                height: 200,
                store: st_users,
                displayField: 'username',
                valueField: 'pk'
            },{
				legend: "Team Managers",
                width: 200,
                height: 200,
                store: new Ext.data.ArrayStore({ data: [ ], fields: ['pk', 'path']}),
                displayField: 'username',
                valueField: 'pk'
	        }]
		},

		{ xtype: "textfield", fieldLabel: "Project Sponsor", name: "project_sponsor" },
		{ xtype: "textarea", fieldLabel: "Project Description", name: "project_description", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Business Case", name: "business_case", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Business Benefits", name: "business_benefits", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Project Scope", name: "project_scope", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Exclusions", name: "exclusions", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH },
		{ xtype: "textarea", fieldLabel: "Assumptions", name: "assumptions", height: TEXTAREA_HEIGHT, width: TEXTAREA_WIDTH } ]
	var project_initiation_form = new Ext.form.FormPanel({url: "/Projects/" + project_number + "/Edit/EditPID/", bodyStyle: "padding: 15px;", autoScroll: true, items: project_initiation_fields });
	project_initiation_form.getForm().load({ url: "/xhr/" + project_number + "/edit_pid", method: "GET" });
	var pid_win = new Ext.Window({width: 620, height:540, closeAction: "hide", autoScroll: true, modal: true, title: "Edit Project Initiation", items: [ project_initiation_form ],
							buttons: [ { text: 'Save',
                                         handler: function(){
                                         project_initiation_form.getForm().submit({
                                            success: function(f,a){
                                            Ext.Msg.alert('Success', 'Project Initiation Update', function() { pid_win.hide(); window.location.reload();});
					    },  
                                            failure: function(f,a){
                                            Ext.Msg.alert('Warning', 'An Error occured');
                                            }
                                        });

					 
                                        }}   
									, { text: 'Close', handler: function(){ pid_win.hide(); } }] });
	project_menu.hide();
	tabpanel.activate(0);
	pid_win.show();
}




/*
 *
 * Build the Project Management menu 
 *
 * */
var project_menu =  new Ext.menu.Menu({	items: [{ text: "Add Deliverable", handler: add_deliverable}, 
											{ text: "Add Risk", handler: add_risk },
											{ text: "Add Issue", handler: add_issue },
											{ text: "Add Lesson Learnt", href: "/WIP/NEW" },
											{ text: "Add Report", href: "/WIP/NEW" },
											{ text: "Add File", href: "/WIP/NEW" },
											{ text: "Edit Project Initiation", handler: edit_project_initiation },
											{ text: "Edit Work Breakdown Structure", handler: edit_project_initiation } ]});
var project_menu_button = { xtype: "tbbutton", text: "Manage Project", menu: project_menu }
toolbar.add(project_menu_button); 

/* 
 *
 * Create tabs 
 *
 * */
tab_items = [
	{ xtype: "panel", contentEl: "project_initiation", title: "Project Initiation" },
	{ xtype: "panel", title: "Deliverables", items: [ panel_deliverables ] },
	{ xtype: "panel", title: "Risks", items: [ risk_panel ] },
	{ xtype: "panel", title: "Work Items", items: [ panel_wbs ] },
	{ xtype: "panel", title: "Issues", items: [ panel_issues ] },
	{ xtype: "panel", title: "Lessons Learnt", items: [ panel_lessons ] },
	{ xtype: "panel", title: "Reports", items: [ panel_report ] },
	{ xtype: "panel", contentEl: "project_files", title: "Files" } ]

var tabpanel = new Ext.TabPanel({ items: tab_items, bodyStyle: "padding: 15px;", activeTab: 0});	
center_panel.items = [ toolbar, tabpanel ]
