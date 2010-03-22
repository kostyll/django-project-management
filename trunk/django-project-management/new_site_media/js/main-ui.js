var tree_data = [
					{ text: 'Projects', leaf: false,
						children: [{ text: 'View Dashboard', href: "/", leaf: true }, { text: "All Projects", href: "/AllProjects", leaf: true }] },
  					{ text: 'Work In Progress', leaf: false,
    					children: [{ text: "All WIP Reports", href: "/WIP", leaf: true}, { text: "Your WIP Items", href: "/YourWIP", leaf: true}] },
  					{ text: 'Rota', leaf: false,
    					children: [{ text: "All Rotas", href: "/AllWIPReports", leaf: true}, { text: "Your Rota", href: "/YourWIP", leaf: true},
    					{ text: "Your Teams Rota", href: "/AllWIPReports", leaf: true} ]},
  					{ text: 'Skillsets', leaf: false,
    					children: [{ text: "View Matrix", href: "/YourWIP", leaf: true}] }
				]

var rootNode = new Ext.tree.AsyncTreeNode({ text: 'Root', children: tree_data });
var tree = new Ext.tree.TreePanel({ root: rootNode, border: false, rootVisible: false, stateful: true, stateId: "nav_tree" });
var center_html_content = { xtype: "panel", contentEl: "center_panel_html", bodyStyle: "padding: 15px;"}
var new_menu = { xtype: "tbbutton", text: "New", menu: [{ text: "New Project", href: "/Projects/New"}, { text: "New WIP Report", href: "/WIP/NEW" }]}
var toolbar = new Ext.Toolbar({ items: [ new_menu ] });

var center_panel = { xtype: "panel", region: "center", title: "WTMS Traffic", items: [ toolbar, center_html_content ], bodyStyle: "padding: 0px;"}
var west_panel = { xtype: "panel", title: 'Navigation', region: 'west', margins: '0 0 0 0',
					cmargins: '0 5 0 0', width: 175, minSize: 100, maxSize: 250, items: [ tree ] }




