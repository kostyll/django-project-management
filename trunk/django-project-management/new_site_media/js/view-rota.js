Ext.QuickTips.init();

/* Some constants used in forms and grids */
var GRID_HEIGHT = 210
var GRID_WIDTH = 500
var TEXTAREA_WIDTH = 400
var TEXTAREA_HEIGHT = 80 

/* 
 * Some reusable functions
 *
 */

var dateValue = "";

var st_users = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Rota/Users/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"username", mapping: "extras.get_full_name"}]}),
//	autoLoad: true
});

var st_rota_activities = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: "/Rota/RotaActivities/" }),
	reader: new Ext.data.JsonReader({ root: "", fields: [{name:"pk", mapping: "pk"},{name:"activity", mapping: "fields.activity"}]}),
//	autoLoad: true
});

var st_rota_items = new Ext.data.Store({
	proxy: new Ext.data.HttpProxy({ url: rota_url + dateValue }),
	reader: new Ext.data.JsonReader({ root: "", fields: [
		{name:"pk", mapping: "pk"},
		{name:"user", mapping: "user"},
		{name:"monday", mapping: "1_r"},
		{name:"tuesday", mapping: "2_r"},
		{name:"wednesday", mapping: "3_r"},
		{name:"thursday", mapping: "4_r"},
		{name:"friday", mapping: "5_r"},
		{name:"saturday", mapping: "6_r"},
		{name:"sunday", mapping: "7_r"}
		]}),
	autoLoad: true
});

var editor = new Ext.ux.grid.RowEditor({
        saveText: 'Update'
    });
    
    
var grid_rota = new Ext.grid.GridPanel({
        store: st_rota_items,
        columns: [
            {header: "pk", dataIndex: 'pk', sortable: true, hidden: true},
            {header: "User", dataIndex: 'user', sortable: true},
            {header: "Monday", dataIndex: 'monday', sortable: true },
            {header: "Tuesday", dataIndex: 'tuesday', sortable: true},
            {header: "Wednesday", dataIndex: 'wednesday', sortable: true},
            {header: "Thursday", dataIndex: 'thursday', sortable: true},
            {header: "Friday", dataIndex: 'friday', sortable: true},
            {header: "Saturday", dataIndex: 'saturday', sortable: true},
            {header: "Sunday", dataIndex: 'sunday', sortable: true}],
        tbar: [{
        xtype: "fieldset",
        iconCls: "icon-user",
        defaultType: "datefield",
        labelAlign: "left",
        items: [{
           fieldLabel: 'Select Date',
           name: 'rotadate',
           id: 'rotadate',
           width: 100,
           listeners: {
           	select: function(picker,date_string){
           		var chosen_date = new Date(date_string);
           		var year = chosen_date.getFullYear();
           		var month = chosen_date.getMonth() + 1;
           		var day = chosen_date.getDate();
           		
           		st_rota_items.proxy = new Ext.data.HttpProxy({ url: rota_url + year + "/" + month + "/" + day + "/" }),
           		st_rota_items.load()
           		}
          }
           }]
           
      }],
		//sm: new Ext.grid.RowSelectionModel({singleSelect: true}),
		viewConfig: { forceFit: true },
		plugin: [editor],
        height: GRID_HEIGHT,
        id:'grid_rotas',
		width: GRID_WIDTH,
		split: true,
		region: 'center'
});

var panel_rota = new Ext.Panel({
	layout: 'border', height: 400,
	items: [ grid_rota ]
});



tab_items = [
	{ xtype: "panel", title: "Rota", items: [ panel_rota ] }
	]

var tabpanel = new Ext.TabPanel({ items: tab_items, bodyStyle: "padding: 15px;", activeTab: 0});	
center_panel.items = [ panel_rota ]
