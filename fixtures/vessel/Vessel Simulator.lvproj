<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="21008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">false</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Slave Modules" Type="Folder">
			<Item Name="Corvus" Type="Folder">
				<Item Name="Custom MB Datatypes" Type="Folder">
					<Item Name="Corvus Byte Datatype.lvclass" Type="LVClass" URL="../Slave Modules/Custom MB Datatypes/Corvus Byte Datatype/Corvus Byte Datatype.lvclass"/>
				</Item>
				<Item Name="Battery Pack.lvclass" Type="LVClass" URL="../Slave Modules/Battery Pack/Battery Pack.lvclass"/>
			</Item>
			<Item Name="Danfoss" Type="Folder">
				<Item Name="iC7-AFE.lvclass" Type="LVClass" URL="../iC7-AFE/iC7-AFE.lvclass"/>
				<Item Name="iC7-DCDC.lvclass" Type="LVClass" URL="../iC7-DCDC/iC7-DCDC.lvclass"/>
				<Item Name="iC7-INU.lvclass" Type="LVClass" URL="../iC7-INU/iC7-INU.lvclass"/>
				<Item Name="Vacon-DCGuard.lvclass" Type="LVClass" URL="../Vacon-DCGuard/Vacon-DCGuard.lvclass"/>
			</Item>
			<Item Name="ComAp" Type="Folder">
				<Item Name="ComAp-Generator.lvclass" Type="LVClass" URL="../ComAp-Generator/ComAp-Generator.lvclass"/>
			</Item>
			<Item Name="MB Slave Simulator Base.lvclass" Type="LVClass" URL="../MB Slave Simulator Base/MB Slave Simulator Base.lvclass"/>
		</Item>
		<Item Name="launcher.lvclass" Type="LVClass" URL="../Launcher/launcher.lvclass"/>
		<Item Name="Sim DiscreteIO.lvclass" Type="LVClass" URL="../Sim DiscreteIO/Sim DiscreteIO.lvclass"/>
		<Item Name="Formulas Module.lvclass" Type="LVClass" URL="../Formulas Module/Formulas Module.lvclass"/>
		<Item Name="Global.vi" Type="VI" URL="../Global.vi"/>
		<Item Name="Splash Screen.vi" Type="VI" URL="../Splash Screen.vi"/>
		<Item Name="Pre-Build Action.vi" Type="VI" URL="../Pre-Build Action.vi"/>
		<Item Name="version.vi" Type="VI" URL="../version.vi"/>
		<Item Name="WS" Type="Web Service">
			<Property Name="Bld_buildSpecName" Type="Str"></Property>
			<Property Name="Bld_version.build" Type="Int">66</Property>
			<Property Name="ws.autoIncrementVersion" Type="Bool">true</Property>
			<Property Name="ws.disconnectInline" Type="Bool">true</Property>
			<Property Name="ws.disconnectTypeDefs" Type="Bool">false</Property>
			<Property Name="ws.guid" Type="Str">{1B690E30-CB44-4FFF-8A44-657AA95E5DC5}</Property>
			<Property Name="ws.modifyLibraryFile" Type="Bool">true</Property>
			<Property Name="ws.privilege_role_map_size" Type="Int">0</Property>
			<Property Name="ws.remoteDebugging" Type="Bool">false</Property>
			<Property Name="ws.removeLibraryItems" Type="Bool">true</Property>
			<Property Name="ws.removePolyVIs" Type="Bool">true</Property>
			<Property Name="ws.serveDefaultDoc" Type="Bool">true</Property>
			<Property Name="ws.SSE2" Type="Bool">true</Property>
			<Property Name="ws.static_permissions" Type="Str"></Property>
			<Property Name="ws.version.build" Type="Int">66</Property>
			<Property Name="ws.version.fix" Type="Int">0</Property>
			<Property Name="ws.version.major" Type="Int">1</Property>
			<Property Name="ws.version.minor" Type="Int">0</Property>
			<Item Name="Startup VIs" Type="Startup VIs Container"/>
			<Item Name="Web Resources" Type="HTTP WebResources Container">
				<Item Name="get" Type="HTTP WebResources Container">
					<Item Name="data.vi" Type="VI" URL="../WS/data.vi">
						<Property Name="ws.buffered" Type="Bool">true</Property>
						<Property Name="ws.includeNameInURL" Type="Bool">true</Property>
						<Property Name="ws.keepInMemory" Type="Bool">true</Property>
						<Property Name="ws.loadAtStartup" Type="Bool">true</Property>
						<Property Name="ws.method" Type="Int">1</Property>
						<Property Name="ws.outputFormat" Type="Int">4</Property>
						<Property Name="ws.outputType" Type="Int">1</Property>
						<Property Name="ws.permissions" Type="Str"></Property>
						<Property Name="ws.requireAPIKey" Type="Bool">false</Property>
						<Property Name="ws.requiredPrivilege" Type="Str"></Property>
						<Property Name="ws.type" Type="Int">1</Property>
						<Property Name="ws.uri" Type="Str"></Property>
						<Property Name="ws.useHeaders" Type="Bool">true</Property>
						<Property Name="ws.useStandardURL" Type="Bool">true</Property>
					</Item>
				</Item>
				<Item Name="post" Type="HTTP WebResources Container">
					<Item Name="cmd.vi" Type="VI" URL="../WS/cmd.vi">
						<Property Name="ws.buffered" Type="Bool">true</Property>
						<Property Name="ws.includeNameInURL" Type="Bool">true</Property>
						<Property Name="ws.keepInMemory" Type="Bool">true</Property>
						<Property Name="ws.loadAtStartup" Type="Bool">true</Property>
						<Property Name="ws.method" Type="Int">3</Property>
						<Property Name="ws.outputFormat" Type="Int">4</Property>
						<Property Name="ws.outputType" Type="Int">1</Property>
						<Property Name="ws.permissions" Type="Str"></Property>
						<Property Name="ws.requireAPIKey" Type="Bool">false</Property>
						<Property Name="ws.requiredPrivilege" Type="Str"></Property>
						<Property Name="ws.type" Type="Int">1</Property>
						<Property Name="ws.uri" Type="Str"></Property>
						<Property Name="ws.useHeaders" Type="Bool">true</Property>
						<Property Name="ws.useStandardURL" Type="Bool">true</Property>
					</Item>
				</Item>
			</Item>
		</Item>
		<Item Name="Dependencies" Type="Dependencies">
			<Property Name="NI.SortType" Type="Int">1</Property>
			<Item Name="user.lib" Type="Folder">
				<Property Name="NI.SortType" Type="Int">1</Property>
				<Item Name="Alarms Events.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Alarms and Events Toolkit/Alarms/Alarms Events.lvclass"/>
				<Item Name="Alarms_Global.vi" Type="VI" URL="/&lt;userlib&gt;/S2 Labs/Alarms and Events Toolkit/Alarms_Global.vi"/>
				<Item Name="Callback Notifier.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Queued State Machine/Callback Notifier/Callback Notifier.lvclass"/>
				<Item Name="Configuration.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/ConfigFile/Configuration.lvclass"/>
				<Item Name="Custom Datatype.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/Custom Datatype/Custom Datatype.lvclass"/>
				<Item Name="CVT.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/CVT Toolkit/CVT.lvclass"/>
				<Item Name="Endianness Type.ctl" Type="VI" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/TypeDefs/Endianness Type.ctl"/>
				<Item Name="Error Reporting.lvlib" Type="Library" URL="/&lt;userlib&gt;/S2 Labs/Error Reporting/Error Reporting.lvlib"/>
				<Item Name="File Rotate.vi" Type="VI" URL="/&lt;userlib&gt;/S2 Labs/File IO Toolkit/File Rotate.vi"/>
				<Item Name="Formulas Base.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/Modules/Formulas/Formulas Base.lvclass"/>
				<Item Name="Global Control.ctl" Type="VI" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/Modules/Global Control.ctl"/>
				<Item Name="Interpolate XY.vi" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Numeric and Math/Interpolate XY.vi"/>
				<Item Name="Logging Module.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/Modules/Logging/Logging Module.lvclass"/>
				<Item Name="Logging.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Logging Toolkit/Logging.lvclass"/>
				<Item Name="Modbus Slave Base.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/Modules/Modbus/Modbus Slave Base/Modbus Slave Base.lvclass"/>
				<Item Name="Module.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Module Framework/Modules/Base/Module.lvclass"/>
				<Item Name="openg_array.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/array/array.llb/openg_array.lvlib"/>
				<Item Name="openg_comparison__ogtk.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/comparison/comparison.llb/openg_comparison__ogtk.lvlib"/>
				<Item Name="openg_error.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/error/error.llb/openg_error.lvlib"/>
				<Item Name="openg_file.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/openg_file.lvlib"/>
				<Item Name="openg_string.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/string/string.llb/openg_string.lvlib"/>
				<Item Name="openg_variant.lvlib" Type="Library" URL="/&lt;userlib&gt;/_OpenG.lib/lvdata/lvdata.llb/openg_variant.lvlib"/>
				<Item Name="QSM.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Queued State Machine/QSM.lvclass"/>
				<Item Name="S2L Data Model.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/S2L Data Model/S2L Data Model.lvclass"/>
				<Item Name="S2L Modbus API.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/S2L Modbus API.lvclass"/>
				<Item Name="S2L Modbus Master.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/Master/S2L Modbus Master.lvclass"/>
				<Item Name="S2L Modbus Slave.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/Slave/S2L Modbus Slave.lvclass"/>
				<Item Name="S2L TCP Master.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/TCP Master/S2L TCP Master.lvclass"/>
				<Item Name="S2L TCP Slave.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Modbus Toolkit/TCP Slave/S2L TCP Slave.lvclass"/>
				<Item Name="TDMS.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Logging Toolkit/TDMS/TDMS.lvclass"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Property Name="NI.SortType" Type="Int">1</Property>
				<Item Name="Add File to Zip.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Add File to Zip.vi"/>
				<Item Name="Application Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Application Directory.vi"/>
				<Item Name="Assert Floating-Point Numeric Type.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/TypeAssert/Assert Floating-Point Numeric Type.vim"/>
				<Item Name="Base64 Support.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/Base64/Base64 Support.lvlib"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Close Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Close Zip File.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Create Directory Recursive.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Create Directory Recursive.vi"/>
				<Item Name="Create NI GUID.vi" Type="VI" URL="/&lt;vilib&gt;/string/Create NI GUID.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="Find First Error.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find First Error.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="FormatTime String.vi" Type="VI" URL="/&lt;vilib&gt;/express/express execution control/ElapsedTimeBlock.llb/FormatTime String.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Get File Extension.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get File Extension.vi"/>
				<Item Name="Get File System Separator.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/sysinfo.llb/Get File System Separator.vi"/>
				<Item Name="Get LV Class Default Value By Name.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/LVClass/Get LV Class Default Value By Name.vi"/>
				<Item Name="Get LV Class Name.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/LVClass/Get LV Class Name.vi"/>
				<Item Name="Get Memory Status.vi" Type="VI" URL="/&lt;vilib&gt;/MemoryControl/Get Memory Status.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Get VI Library File Info.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get VI Library File Info.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Has LLB Extension.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Has LLB Extension.vi"/>
				<Item Name="Is Path and Not Empty.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Is Path and Not Empty.vi"/>
				<Item Name="Is Value Changed.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/Is Value Changed.vim"/>
				<Item Name="JDP Timestamp.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/Timestamp/JDP Timestamp.lvlib"/>
				<Item Name="JDP Utility.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/JDP Utility.lvlib"/>
				<Item Name="JSONtext LVClass Serializer.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/JDP Science/JSONtext/LVClass Serializer/JSONtext LVClass Serializer.lvclass"/>
				<Item Name="JSONtext.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JSONtext/JSONtext.lvlib"/>
				<Item Name="libmuparser-lv.dll" Type="Document" URL="/&lt;vilib&gt;/LAVA/muParser/mupLib/libmuparser-lv.dll"/>
				<Item Name="Librarian File Info In.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File Info In.ctl"/>
				<Item Name="Librarian File Info Out.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File Info Out.ctl"/>
				<Item Name="Librarian File List.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File List.ctl"/>
				<Item Name="Librarian Get Info.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian Get Info.vi"/>
				<Item Name="Librarian Path Location.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian Path Location.vi"/>
				<Item Name="Librarian Set Info.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian Set Info.vi"/>
				<Item Name="Librarian.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian.vi"/>
				<Item Name="List Directory and LLBs.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/List Directory and LLBs.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LV70DateRecToTimeStamp.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/LV70DateRecToTimeStamp.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="LVDateTimeRec.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVDateTimeRec.ctl"/>
				<Item Name="LVMapReplaceAction.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVMapReplaceAction.ctl"/>
				<Item Name="LVNumericRepresentation.ctl" Type="VI" URL="/&lt;vilib&gt;/numeric/LVNumericRepresentation.ctl"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="Modbus Master.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/Modbus/master/Modbus Master.lvclass"/>
				<Item Name="Modbus Slave.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/Modbus/slave/Modbus Slave.lvclass"/>
				<Item Name="mupExpr.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/LAVA/muParser/mupExpr/mupExpr.lvclass"/>
				<Item Name="mupLib.lvlib" Type="Library" URL="/&lt;vilib&gt;/LAVA/muParser/mupLib/mupLib.lvlib"/>
				<Item Name="New Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/New Zip File.vi"/>
				<Item Name="NI_Data Type.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/Data Type/NI_Data Type.lvlib"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="NI_PtbyPt.lvlib" Type="Library" URL="/&lt;vilib&gt;/ptbypt/NI_PtbyPt.lvlib"/>
				<Item Name="NI_WebServices.lvlib" Type="Library" URL="/&lt;vilib&gt;/wsapi/NI_WebServices.lvlib"/>
				<Item Name="nisyscfg.lvlib" Type="Library" URL="/&lt;vilib&gt;/nisyscfg/nisyscfg.lvlib"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Path To Command Line String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Path To Command Line String.vi"/>
				<Item Name="PathToUNIXPathString.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/CFURL.llb/PathToUNIXPathString.vi"/>
				<Item Name="Qualified Name Array To Single String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/LVClass/Qualified Name Array To Single String.vi"/>
				<Item Name="Recursive File List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Recursive File List.vi"/>
				<Item Name="Relative Path To Platform Independent String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Relative Path To Platform Independent String.vi"/>
				<Item Name="Remove Duplicates From 1D Array.vim" Type="VI" URL="/&lt;vilib&gt;/Array/Remove Duplicates From 1D Array.vim"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Set Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Busy.vi"/>
				<Item Name="Set Cursor (Cursor ID).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Cursor ID).vi"/>
				<Item Name="Set Cursor (Icon Pict).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Icon Pict).vi"/>
				<Item Name="Set Cursor.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="Set VI Library File Info.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Set VI Library File Info.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
				<Item Name="subElapsedTime.vi" Type="VI" URL="/&lt;vilib&gt;/express/express execution control/ElapsedTimeBlock.llb/subElapsedTime.vi"/>
				<Item Name="SubVIs.lvlib" Type="Library" URL="/&lt;vilib&gt;/Modbus/subvis/SubVIs.lvlib"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="UDP Multicast Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Open.vi"/>
				<Item Name="UDP Multicast Read-Only Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Read-Only Open.vi"/>
				<Item Name="UDP Multicast Read-Write Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Read-Write Open.vi"/>
				<Item Name="UDP Multicast Write-Only Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Write-Only Open.vi"/>
				<Item Name="UID to GObject Reference.vi" Type="VI" URL="/&lt;vilib&gt;/VIServer/UID to GObject Reference.vi"/>
				<Item Name="Unset Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Unset Busy.vi"/>
				<Item Name="VariantType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/VariantDataType/VariantType.lvlib"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
			</Item>
			<Item Name="FPGA_9045.lvbitx" Type="Document" URL="../../cRIO_Argus-Hybrid-Vessel/FPGA Bitfiles/FPGA_9045.lvbitx"/>
			<Item Name="Kernel32.dll" Type="Document" URL="Kernel32.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="LV Config Read Boolean.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Boolean.vi"/>
			<Item Name="LV Config Read Color.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Color.vi"/>
			<Item Name="LV Config Read Numeric (I32).vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Numeric (I32).vi"/>
			<Item Name="LV Config Read Pathlist.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Pathlist.vi"/>
			<Item Name="LV Config Read String.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read String.vi"/>
			<Item Name="LV Config Read.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read.vi"/>
			<Item Name="mscorlib" Type="VI" URL="mscorlib">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="NiFpgaLv.dll" Type="Document" URL="NiFpgaLv.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Replace NaNs.vim" Type="VI" URL="../SubVIs/Replace NaNs.vim"/>
			<Item Name="Rising Edge Detect.vi" Type="VI" URL="../SubVIs/Rising Edge Detect.vi"/>
			<Item Name="System" Type="VI" URL="System">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="System.Management" Type="Document" URL="System.Management">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="systemLogging.dll" Type="Document" URL="systemLogging.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="ws_runtime.dll" Type="Document" URL="ws_runtime.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Vessel Sim" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{2A4376F2-22D7-4D39-B154-9B6AB165E21C}</Property>
				<Property Name="App_INI_GUID" Type="Str">{E8A71EDB-61C7-43BC-B3A7-C25247C35A93}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8010</Property>
				<Property Name="App_serverType" Type="Int">1</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{DC27F6B5-4434-483B-8EE6-C0CC5CE6685F}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Vessel Sim</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../_Builds</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToProject</Property>
				<Property Name="Bld_preActionVIID" Type="Ref">/My Computer/Pre-Build Action.vi</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{1B845042-11AF-4923-9129-3D8ABDEFB5B8}</Property>
				<Property Name="Bld_version.build" Type="Int">48</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">VesselSim.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../_Builds/VesselSim.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">relativeToProject</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../_Builds/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">relativeToProject</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{BDC07AAC-1DAA-4C11-8471-3C708E16BB7D}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Splash Screen.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/launcher.lvclass/Overrides/Modules Catalog.vi</Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[2].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">3</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Vessel Sim</Property>
				<Property Name="TgtF_internalName" Type="Str">Vessel Sim</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2022 </Property>
				<Property Name="TgtF_productName" Type="Str">Vessel Sim</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{324694A1-342A-4E06-9941-AB610ACA0D62}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">VesselSim.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
