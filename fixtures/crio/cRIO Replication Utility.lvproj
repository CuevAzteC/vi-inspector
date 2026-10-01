<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="21008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="IOScan.Faults" Type="Str"></Property>
		<Property Name="IOScan.NetVarPeriod" Type="UInt">100</Property>
		<Property Name="IOScan.NetWatchdogEnabled" Type="Bool">false</Property>
		<Property Name="IOScan.Period" Type="UInt">10000</Property>
		<Property Name="IOScan.PowerupMode" Type="UInt">0</Property>
		<Property Name="IOScan.Priority" Type="UInt">9</Property>
		<Property Name="IOScan.ReportModeConflict" Type="Bool">true</Property>
		<Property Name="IOScan.StartEngineOnDeploy" Type="Bool">false</Property>
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
		<Item Name="Retrieve" Type="Folder">
			<Property Name="NI.SortType" Type="Int">3</Property>
			<Item Name="RetrieveImage_Main.vi" Type="VI" URL="../subVIs/RetrieveImage_Main.vi"/>
			<Item Name="Retrieve_GetTargetImageInfo.vi" Type="VI" URL="../subVIs/Retrieve_GetTargetImageInfo.vi"/>
			<Item Name="Retrieve_SetImageProperties.vi" Type="VI" URL="../subVIs/Retrieve_SetImageProperties.vi"/>
			<Item Name="Retrieve_GetInstalledSoftware.vi" Type="VI" URL="../subVIs/Retrieve_GetInstalledSoftware.vi"/>
			<Item Name="Retrieve_GetImage.vi" Type="VI" URL="../subVIs/Retrieve_GetImage.vi"/>
			<Item Name="Retrieve_PackageImage.vi" Type="VI" URL="../subVIs/Retrieve_PackageImage.vi"/>
		</Item>
		<Item Name="Deploy" Type="Folder">
			<Item Name="DeployImage_Main.vi" Type="VI" URL="../subVIs/DeployImage_Main.vi"/>
			<Item Name="Deploy-ExtractImage.vi" Type="VI" URL="../subVIs/Deploy-ExtractImage.vi"/>
			<Item Name="Deploy_DisplayImageInfo.vi" Type="VI" URL="../Deploy_DisplayImageInfo.vi"/>
			<Item Name="Deploy_SetImage.vi" Type="VI" URL="../subVIs/Deploy_SetImage.vi"/>
		</Item>
		<Item Name="Network" Type="Folder">
			<Item Name="Network_Main.vi" Type="VI" URL="../subVIs/Network_Main.vi"/>
			<Item Name="Network_ApplyDHCP.vi" Type="VI" URL="../subVIs/Network_ApplyDHCP.vi"/>
			<Item Name="Network_ApplyStatic.vi" Type="VI" URL="../subVIs/Network_ApplyStatic.vi"/>
		</Item>
		<Item Name="subVIs" Type="Folder">
			<Item Name="open_sysconfig_session.vi" Type="VI" URL="../subVIs/open_sysconfig_session.vi"/>
			<Item Name="rad_IPaddr and Password Global.vi" Type="VI" URL="../subVIs/rad_IPaddr and Password Global.vi"/>
			<Item Name="rad_UnForceSafeMode.vi" Type="VI" URL="../subVIs/rad_UnForceSafeMode.vi"/>
		</Item>
		<Item Name="TypeDefs" Type="Folder">
			<Item Name="AppImageProperties.ctl" Type="VI" URL="../TypeDefs/AppImageProperties.ctl"/>
			<Item Name="DevInfo.ctl" Type="VI" URL="../TypeDefs/DevInfo.ctl"/>
			<Item Name="FPGA_Properties_Element.ctl" Type="VI" URL="../TypeDefs/FPGA_Properties_Element.ctl"/>
			<Item Name="RetrieveImageStates.ctl" Type="VI" URL="../TypeDefs/RetrieveImageStates.ctl"/>
			<Item Name="TargetAccess.ctl" Type="VI" URL="../TypeDefs/TargetAccess.ctl"/>
			<Item Name="DeployImageStates.ctl" Type="VI" URL="../TypeDefs/DeployImageStates.ctl"/>
		</Item>
		<Item Name="Firmware" Type="Folder">
			<Item Name="UpgradeFirmware.vi" Type="VI" URL="../subVIs/UpgradeFirmware.vi"/>
			<Item Name="UpgradeFirmware_Main.vi" Type="VI" URL="../subVIs/UpgradeFirmware_Main.vi"/>
		</Item>
		<Item Name="Feeds" Type="Folder">
			<Item Name="Feed_Main.vi" Type="VI" URL="../subVIs/Feed_Main.vi"/>
		</Item>
		<Item Name="CardMode" Type="Folder"/>
		<Item Name="S2-Labs-Icon.ico" Type="Document" URL="../S2-Labs-Icon.ico"/>
		<Item Name="Main_old.vi" Type="VI" URL="../Main_old.vi"/>
		<Item Name="Pre-Build Action.vi" Type="VI" URL="../Pre-Build Action.vi"/>
		<Item Name="version.vi" Type="VI" URL="../version.vi"/>
		<Item Name="FeedSM_States.ctl" Type="VI" URL="../subVIs/FeedSM_States.ctl"/>
		<Item Name="tester.vi" Type="VI" URL="../tester.vi"/>
		<Item Name="Main.vi" Type="VI" URL="../Main.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="user.lib" Type="Folder">
				<Item Name="ZLIB File Info__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB File Info__ogtk.ctl"/>
				<Item Name="ZLIB Open ZIP Mode__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Open ZIP Mode__ogtk.ctl"/>
				<Item Name="ZLIB Zip Handle__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Zip Handle__ogtk.ctl"/>
				<Item Name="lvzlib.dll" Type="Document" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzlib.dll"/>
				<Item Name="ZLIB Close Zip Archive__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Close Zip Archive__ogtk.vi"/>
				<Item Name="ZLIB CRC32__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB CRC32__ogtk.vi"/>
				<Item Name="ZLIB Open Zip Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Open Zip Stream__ogtk.vi"/>
				<Item Name="ZLIB Open Zip__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Open Zip__ogtk.vi"/>
				<Item Name="ZLIB Store__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Store__ogtk.vi"/>
				<Item Name="ZLIB Unzip Handle__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Unzip Handle__ogtk.ctl"/>
				<Item Name="ZLIB Open Unzip Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Open Unzip Stream__ogtk.vi"/>
				<Item Name="ZLIB Open Unzip__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Open Unzip__ogtk.vi"/>
				<Item Name="ZLIB Close Unzip Archive__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Close Unzip Archive__ogtk.vi"/>
				<Item Name="ZLIB Get Global Info__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Get Global Info__ogtk.vi"/>
				<Item Name="ZLIB Extract All Files To Dir__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Extract All Files To Dir__ogtk.vi"/>
				<Item Name="Error Reporting.lvlib" Type="Library" URL="/&lt;userlib&gt;/S2 Labs/Error Reporting/Error Reporting.lvlib"/>
				<Item Name="Callback Notifier.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Queued State Machine/Callback Notifier/Callback Notifier.lvclass"/>
				<Item Name="QSM.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/S2 Labs/Queued State Machine/QSM.lvclass"/>
				<Item Name="Two-Way Comparison Versus Array Element No Class.vim" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/Sorted Search Support/Two-Way Comparison Versus Array Element No Class.vim"/>
				<Item Name="Search Sorted 1D Array No Class.vim" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/Sorted Search Support/Search Sorted 1D Array No Class.vim"/>
				<Item Name="Search Sorted 1D Array Index and Length.vim" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/Search Sorted 1D Array Index and Length.vim"/>
				<Item Name="Enum - Order Ascending Descending.ctl" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/Controls/Enum - Order Ascending Descending.ctl"/>
				<Item Name="Sort 1D Array-VIM.vim" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/OpenG/Sort 1D Array-VIM.vim"/>
				<Item Name="Search 1D Array-VIM.vim" Type="VI" URL="/&lt;userlib&gt;/_Hooovahh/Array VIMs/OpenG/Search 1D Array-VIM.vim"/>
				<Item Name="ZLIB Open Zip Archive (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Zip Archive (Wide Path)__ogtk.vi"/>
				<Item Name="PATH Refnum__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/PATH Refnum__ogtk.ctl"/>
				<Item Name="ZLIB Open Zip Archive (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Zip Archive (Path)__ogtk.vi"/>
				<Item Name="FILE Create Wide Path (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Wide Path (Path)__ogtk.vi"/>
				<Item Name="ZLIB Store File (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store File (Path)__ogtk.vi"/>
				<Item Name="ZLIB Store Options__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/ZLIB Store Options__ogtk.ctl"/>
				<Item Name="ZLIB Unicode Type__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Unicode Type__ogtk.ctl"/>
				<Item Name="ZLIB Specific Path to Common Path (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Specific Path to Common Path (Path)__ogtk.vi"/>
				<Item Name="ZLIB Specific Path  to Common Path (String)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Specific Path  to Common Path (String)__ogtk.vi"/>
				<Item Name="ZLIB Store File (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store File (Wide Path)__ogtk.vi"/>
				<Item Name="ZLIB Store File Prepare__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store File Prepare__ogtk.vi"/>
				<Item Name="ZLIB Entry Type__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Entry Type__ogtk.ctl"/>
				<Item Name="ZLIB Build Extra Field Data__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Build Extra Field Data__ogtk.vi"/>
				<Item Name="ZLIB File Information__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB File Information__ogtk.vi"/>
				<Item Name="FILE Parent Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Parent Path__ogtk.vi"/>
				<Item Name="FILE Parent Path (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Parent Path (UTF8)__ogtk.vi"/>
				<Item Name="FILE Create Wide Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Create Wide Path__ogtk.vi"/>
				<Item Name="FILE Create Wide Path (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Wide Path (UTF8)__ogtk.vi"/>
				<Item Name="FILE Parent Path (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Parent Path (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Convert Wide Path (String)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Convert Wide Path (String)__ogtk.vi"/>
				<Item Name="FILE Parent Path (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Parent Path (Path)__ogtk.vi"/>
				<Item Name="FILE Attributes__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Attributes__ogtk.vi"/>
				<Item Name="FILE Attributes (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Attributes (Path)__ogtk.vi"/>
				<Item Name="FILE Attributes__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Attributes__ogtk.ctl"/>
				<Item Name="FILE Attributes (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Attributes (Wide Path)__ogtk.vi"/>
				<Item Name="UTIL Is Little Endian__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/UTIL Is Little Endian__ogtk.vi"/>
				<Item Name="FILE Attributes (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Attributes (UTF8)__ogtk.vi"/>
				<Item Name="FILE Convert Wide Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Convert Wide Path__ogtk.vi"/>
				<Item Name="FILE Convert Wide Path (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Convert Wide Path (Path)__ogtk.vi"/>
				<Item Name="ZLIB Get File CRC32__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Get File CRC32__ogtk.vi"/>
				<Item Name="FILE Open File Refnum__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Open File Refnum__ogtk.vi"/>
				<Item Name="FILE Open File Refnum (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Open File Refnum (Path)__ogtk.vi"/>
				<Item Name="FILE Refnum__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Refnum__ogtk.ctl"/>
				<Item Name="FILE Open File Refnum (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Open File Refnum (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Open File Refnum (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Open File Refnum (UTF8)__ogtk.vi"/>
				<Item Name="FILE Get Size__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Get Size__ogtk.vi"/>
				<Item Name="ZLIB Block Size__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Block Size__ogtk.vi"/>
				<Item Name="FILE Read Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Read Stream__ogtk.vi"/>
				<Item Name="FILE Close__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Close__ogtk.vi"/>
				<Item Name="ZLIB Open Write File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Write File__ogtk.vi"/>
				<Item Name="ZLIB Compress File Info__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Compress File Info__ogtk.ctl"/>
				<Item Name="ZLIB Method and Level__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Method and Level__ogtk.vi"/>
				<Item Name="STRUTIL Has Extended Characters__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/stringutil.llb/STRUTIL Has Extended Characters__ogtk.vi"/>
				<Item Name="STRUTIL Convert String__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/stringutil.llb/STRUTIL Convert String__ogtk.vi"/>
				<Item Name="ZLIB Store File Continue__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store File Continue__ogtk.vi"/>
				<Item Name="ZLIB File Transfer Info__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB File Transfer Info__ogtk.ctl"/>
				<Item Name="ZLIB Write File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Write File__ogtk.vi"/>
				<Item Name="ZLIB Close Write File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Close Write File__ogtk.vi"/>
				<Item Name="FILE Delete__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Delete__ogtk.vi"/>
				<Item Name="FILE Delete (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Delete (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Delete (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Delete (Path)__ogtk.vi"/>
				<Item Name="FILE Delete (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Delete (UTF8)__ogtk.vi"/>
				<Item Name="ZLIB Store Link__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store Link__ogtk.vi"/>
				<Item Name="FILE Read Link Target__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Read Link Target__ogtk.vi"/>
				<Item Name="FILE Read Link Target (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Read Link Target (Path)__ogtk.vi"/>
				<Item Name="FILE Read Link Target (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Read Link Target (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Read Link Target (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Read Link Target (UTF8)__ogtk.vi"/>
				<Item Name="ZLIB Write Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Write Stream__ogtk.vi"/>
				<Item Name="ZLIB Store Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store Stream__ogtk.vi"/>
				<Item Name="ZLIB Store Directory__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Store Directory__ogtk.vi"/>
				<Item Name="FILE Write Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Write Stream__ogtk.vi"/>
				<Item Name="ZLIB Extract All Files To Dir (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Extract All Files To Dir (Path)__ogtk.vi"/>
				<Item Name="FILE Get Type__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Get Type__ogtk.vi"/>
				<Item Name="FILE Get Type (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Get Type (Wide Path)__ogtk.vi"/>
				<Item Name="PATH Type__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/PATH Type__ogtk.ctl"/>
				<Item Name="FILE Get Type (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Get Type (Path)__ogtk.vi"/>
				<Item Name="FILE Get Type (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Get Type (UTF8)__ogtk.vi"/>
				<Item Name="ZLIB Extract All Files To Dir (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Extract All Files To Dir (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Convert File Extension__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Convert File Extension__ogtk.vi"/>
				<Item Name="FILE Convert File Extension (String)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Convert File Extension (String)__ogtk.vi"/>
				<Item Name="FILE Convert File Extension (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Convert File Extension (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Append Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Append Path__ogtk.vi"/>
				<Item Name="FILE Append Path (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Append Path (UTF8)__ogtk.vi"/>
				<Item Name="FILE Append Path (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Append Path (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Append Path (Wide Paths)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Append Path (Wide Paths)__ogtk.vi"/>
				<Item Name="FILE Append Path (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Append Path (Path)__ogtk.vi"/>
				<Item Name="FILE Create Directory Recursive__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Create Directory Recursive__ogtk.vi"/>
				<Item Name="FILE Create Directory Recursive (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Directory Recursive (UTF8)__ogtk.vi"/>
				<Item Name="FILE Create Directory Recursive (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Directory Recursive (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Create Directory Recursive (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Directory Recursive (Path)__ogtk.vi"/>
				<Item Name="ZLIB Open Unzip Archive (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Unzip Archive (Path)__ogtk.vi"/>
				<Item Name="ZLIB Open Unzip Archive (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Unzip Archive (Wide Path)__ogtk.vi"/>
				<Item Name="ZLIB Go To File Low Level__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Go To File Low Level__ogtk.vi"/>
				<Item Name="ZLIB Uncompress File Info__ogtk.ctl" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Uncompress File Info__ogtk.ctl"/>
				<Item Name="ZLIB Convert File Info__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Convert File Info__ogtk.vi"/>
				<Item Name="ZLIB Parse Extra Field Data__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Parse Extra Field Data__ogtk.vi"/>
				<Item Name="ZLIB Fixup File Attributes__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Fixup File Attributes__ogtk.vi"/>
				<Item Name="ZLIB Common Path to Specific Path (String)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Common Path to Specific Path (String)__ogtk.vi"/>
				<Item Name="ZLIB Get File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Get File__ogtk.vi"/>
				<Item Name="ZLIB Open Read File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Open Read File__ogtk.vi"/>
				<Item Name="ZLIB Read Compressed File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Read Compressed File__ogtk.vi"/>
				<Item Name="ZLIB Read Local Extra Data__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Read Local Extra Data__ogtk.vi"/>
				<Item Name="ZLIB Close Read File__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Close Read File__ogtk.vi"/>
				<Item Name="ZLIB Read Compressed Stream__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Read Compressed Stream__ogtk.vi"/>
				<Item Name="FILE Create Link__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/FILE Create Link__ogtk.vi"/>
				<Item Name="FILE Create Link (Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Link (Path)__ogtk.vi"/>
				<Item Name="FILE Create Link (Wide Path)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Link (Wide Path)__ogtk.vi"/>
				<Item Name="FILE Create Link (UTF8)__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/fileutil.llb/subVIs/FILE Create Link (UTF8)__ogtk.vi"/>
				<Item Name="ZLIB Update File Attributes__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Update File Attributes__ogtk.vi"/>
				<Item Name="ZLIB Extract Timestamps__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/lvzip/lvzip.llb/subVI/ZLIB Extract Timestamps__ogtk.vi"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Librarian File Info In.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File Info In.ctl"/>
				<Item Name="Librarian File Info Out.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File Info Out.ctl"/>
				<Item Name="Librarian File List.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian File List.ctl"/>
				<Item Name="LVNumericRepresentation.ctl" Type="VI" URL="/&lt;vilib&gt;/numeric/LVNumericRepresentation.ctl"/>
				<Item Name="System Directory Type.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/System Directory Type.ctl"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="JSONtext LVClass Serializer.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/JDP Science/JSONtext/LVClass Serializer/JSONtext LVClass Serializer.lvclass"/>
				<Item Name="Base64 Support.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/Base64/Base64 Support.lvlib"/>
				<Item Name="JDP Timestamp.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/Timestamp/JDP Timestamp.lvlib"/>
				<Item Name="JDP Utility.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JDP Science Common Utilities/JDP Utility.lvlib"/>
				<Item Name="JSONtext.lvlib" Type="Library" URL="/&lt;vilib&gt;/JDP Science/JSONtext/JSONtext.lvlib"/>
				<Item Name="NI_Data Type.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/Data Type/NI_Data Type.lvlib"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="nisyscfg.lvlib" Type="Library" URL="/&lt;vilib&gt;/nisyscfg/nisyscfg.lvlib"/>
				<Item Name="Add File to Zip.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Add File to Zip.vi"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Close Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/Close Zip File.vi"/>
				<Item Name="Compare Two Paths.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Compare Two Paths.vi"/>
				<Item Name="Copy In Or Out Of VI Library.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Copy In Or Out Of VI Library.vi"/>
				<Item Name="Create Directory Recursive.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Create Directory Recursive.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="Generate Temporary File Path.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Generate Temporary File Path.vi"/>
				<Item Name="Get File Extension.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get File Extension.vi"/>
				<Item Name="Get System Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/Get System Directory.vi"/>
				<Item Name="Get VI Library File Info.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get VI Library File Info.vi"/>
				<Item Name="Is Path and Not Empty.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Is Path and Not Empty.vi"/>
				<Item Name="Librarian Delete Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian Delete Dialog.vi"/>
				<Item Name="Librarian OK to Delete.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian OK to Delete.vi"/>
				<Item Name="Librarian Path Location.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian Path Location.vi"/>
				<Item Name="Librarian.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Librarian.vi"/>
				<Item Name="List Directory and LLBs.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/List Directory and LLBs.vi"/>
				<Item Name="New Zip File.vi" Type="VI" URL="/&lt;vilib&gt;/zip/New Zip File.vi"/>
				<Item Name="Path To Command Line String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Path To Command Line String.vi"/>
				<Item Name="PathToUNIXPathString.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/CFURL.llb/PathToUNIXPathString.vi"/>
				<Item Name="Prepare VI Library for Copy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Prepare VI Library for Copy.vi"/>
				<Item Name="Recursive File List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Recursive File List.vi"/>
				<Item Name="Relative Path To Platform Independent String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Relative Path To Platform Independent String.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Busy.vi"/>
				<Item Name="Set Cursor (Cursor ID).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Cursor ID).vi"/>
				<Item Name="Set Cursor (Icon Pict).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Icon Pict).vi"/>
				<Item Name="Set Cursor.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor.vi"/>
				<Item Name="subFile Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/express/express input/FileDialogBlock.llb/subFile Dialog.vi"/>
				<Item Name="Temp Backup File.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Temp Backup File.vi"/>
				<Item Name="Temp Filename.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Temp Filename.vi"/>
				<Item Name="Temp Restore File.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Temp Restore File.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Unset Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Unset Busy.vi"/>
				<Item Name="Get LV Class Name.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/LVClass/Get LV Class Name.vi"/>
				<Item Name="NI_Unzip.lvlib" Type="Library" URL="/&lt;vilib&gt;/zip/NI_Unzip.lvlib"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="UDP Multicast Write-Only Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Write-Only Open.vi"/>
				<Item Name="UDP Multicast Read-Write Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Read-Write Open.vi"/>
				<Item Name="UDP Multicast Read-Only Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Read-Only Open.vi"/>
				<Item Name="UDP Multicast Open.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/UDP Multicast Open.vi"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
				<Item Name="UID to GObject Reference.vi" Type="VI" URL="/&lt;vilib&gt;/VIServer/UID to GObject Reference.vi"/>
				<Item Name="8.6CompatibleGlobalVar.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/config.llb/8.6CompatibleGlobalVar.vi"/>
				<Item Name="NI_LVConfig.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/config.llb/NI_LVConfig.lvlib"/>
				<Item Name="LVDateTimeRec.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVDateTimeRec.ctl"/>
			</Item>
			<Item Name="nisyscfg.dll" Type="Document" URL="nisyscfg.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="rad_NI-Auth Login Dialog.vi" Type="VI" URL="../subVIs/rad_NI-Auth Login Dialog.vi"/>
			<Item Name="rad_Open Session.vi" Type="VI" URL="../subVIs/rad_Open Session.vi"/>
			<Item Name="LV Config Read String.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read String.vi"/>
			<Item Name="LV Config Read Numeric (I32).vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Numeric (I32).vi"/>
			<Item Name="LV Config Read Color.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Color.vi"/>
			<Item Name="LV Config Read Pathlist.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Pathlist.vi"/>
			<Item Name="LV Config Read Boolean.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read Boolean.vi"/>
			<Item Name="LV Config Read.vi" Type="VI" URL="/&lt;resource&gt;/dialog/lvconfig.llb/LV Config Read.vi"/>
			<Item Name="systemLogging.dll" Type="Document" URL="systemLogging.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Kernel32.dll" Type="Document" URL="Kernel32.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="System.Management" Type="Document" URL="System.Management">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="mscorlib" Type="VI" URL="mscorlib">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="System" Type="VI" URL="System">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="cRIO Replication Utility" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{E780E2E4-40C6-4B8B-A821-9CB366E7B071}</Property>
				<Property Name="App_INI_GUID" Type="Str">{DD49BB60-0C33-436D-8E3C-9A26DB0969BE}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_serverType" Type="Int">0</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{D52EDB62-B79B-4B2D-9FEE-E59AEBADEC34}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">cRIO Replication Utility</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/zKirby/lv_PC Builds/NI_AB_PROJECTNAME/exe</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_preActionVIID" Type="Ref">/My Computer/Pre-Build Action.vi</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{EB5C0F30-CD2F-4616-9F7E-E3BEC04BA14D}</Property>
				<Property Name="Bld_version.build" Type="Int">1</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Bld_version.patch" Type="Int">2</Property>
				<Property Name="Destination[0].destName" Type="Str">cRIO Replication Utility.exe</Property>
				<Property Name="Destination[0].path" Type="Path">/C/zKirby/lv_PC Builds/NI_AB_PROJECTNAME/exe/cRIO Replication Utility.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/zKirby/lv_PC Builds/NI_AB_PROJECTNAME/exe/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/S2-Labs-Icon.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{0A006D56-2214-47A9-B7AC-71AAC8EA0527}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Main_old.vi</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/Main.vi</Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[2].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">3</Property>
				<Property Name="TgtF_companyName" Type="Str">Stewart &amp; Stevenson | S2 Labs</Property>
				<Property Name="TgtF_fileDescription" Type="Str">cRIO Replication Utility</Property>
				<Property Name="TgtF_internalName" Type="Str">cRIO Replication Utility</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2023 Stewart &amp; Stevenson | S2 Labs</Property>
				<Property Name="TgtF_productName" Type="Str">cRIO Replication Utility</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{BCC7A01B-FDA9-4510-A8BD-25D12CC3A478}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">cRIO Replication Utility.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="cRIO Replication Utitlity" Type="{E661DAE2-7517-431F-AC41-30807A3BDA38}">
				<Property Name="NIPKG_addToFeed" Type="Bool">false</Property>
				<Property Name="NIPKG_allDependenciesToFeed" Type="Bool">false</Property>
				<Property Name="NIPKG_allDependenciesToSystemLink" Type="Bool">false</Property>
				<Property Name="NIPKG_certificates" Type="Bool">true</Property>
				<Property Name="NIPKG_createInstaller" Type="Bool">false</Property>
				<Property Name="NIPKG_feedLocation" Type="Path">../builds/NI_AB_PROJECTNAME/cRIO Replication Utitlity/Feed</Property>
				<Property Name="NIPKG_feedLocation.Type" Type="Str">relativeToCommon</Property>
				<Property Name="NIPKG_installerArtifacts" Type="Str"></Property>
				<Property Name="NIPKG_installerBuiltBefore" Type="Bool">false</Property>
				<Property Name="NIPKG_installerDestination" Type="Path">../builds/NI_AB_PROJECTNAME/cRIO Replication Utitlity/Package Installer</Property>
				<Property Name="NIPKG_installerDestination.Type" Type="Str">relativeToCommon</Property>
				<Property Name="NIPKG_lastBuiltPackage" Type="Str">crio-replication-utility_1.0.2-0_windows_all.nipkg</Property>
				<Property Name="NIPKG_license" Type="Ref"></Property>
				<Property Name="NIPKG_packageVersion" Type="Bool">false</Property>
				<Property Name="NIPKG_releaseNotes" Type="Str"></Property>
				<Property Name="NIPKG_storeProduct" Type="Bool">true</Property>
				<Property Name="NIPKG_VisibleForRuntimeDeployment" Type="Bool">false</Property>
				<Property Name="PKG_actions.Count" Type="Int">0</Property>
				<Property Name="PKG_autoIncrementBuild" Type="Bool">true</Property>
				<Property Name="PKG_autoSelectDeps" Type="Bool">false</Property>
				<Property Name="PKG_buildNumber" Type="Int">1</Property>
				<Property Name="PKG_buildSpecName" Type="Str">cRIO Replication Utitlity</Property>
				<Property Name="PKG_dependencies.Count" Type="Int">2</Property>
				<Property Name="PKG_dependencies[0].Enhanced" Type="Bool">false</Property>
				<Property Name="PKG_dependencies[0].MaxVersion" Type="Str"></Property>
				<Property Name="PKG_dependencies[0].MaxVersionInclusive" Type="Bool">false</Property>
				<Property Name="PKG_dependencies[0].MinVersion" Type="Str">21.1.2.49154-0+f2</Property>
				<Property Name="PKG_dependencies[0].MinVersionType" Type="Str">Inclusive</Property>
				<Property Name="PKG_dependencies[0].NIPKG.DisplayName" Type="Str">LabVIEW Runtime (32-bit)</Property>
				<Property Name="PKG_dependencies[0].Package.Name" Type="Str">ni-labview-2021-runtime-engine-x86</Property>
				<Property Name="PKG_dependencies[0].Package.Section" Type="Str">Programming Environments</Property>
				<Property Name="PKG_dependencies[0].Package.Synopsis" Type="Str">The LabVIEW Runtime is a software add-on that enables engineers to run executables on a nondevelopment machine.</Property>
				<Property Name="PKG_dependencies[0].Relationship" Type="Str">Required Dependency</Property>
				<Property Name="PKG_dependencies[0].Type" Type="Str">NIPKG</Property>
				<Property Name="PKG_dependencies[1].Enhanced" Type="Bool">false</Property>
				<Property Name="PKG_dependencies[1].MaxVersion" Type="Str"></Property>
				<Property Name="PKG_dependencies[1].MaxVersionInclusive" Type="Bool">false</Property>
				<Property Name="PKG_dependencies[1].MinVersion" Type="Str">21.5.0.49392-0+f240</Property>
				<Property Name="PKG_dependencies[1].MinVersionType" Type="Str">Inclusive</Property>
				<Property Name="PKG_dependencies[1].NIPKG.DisplayName" Type="Str">NI System Configuration Runtime</Property>
				<Property Name="PKG_dependencies[1].Package.Name" Type="Str">ni-syscfg-runtime</Property>
				<Property Name="PKG_dependencies[1].Package.Section" Type="Str">Runtime</Property>
				<Property Name="PKG_dependencies[1].Package.Synopsis" Type="Str">Run-time components required to deploy applications that use the NI System Configuration API.</Property>
				<Property Name="PKG_dependencies[1].Relationship" Type="Str">Required Dependency</Property>
				<Property Name="PKG_dependencies[1].Type" Type="Str">NIPKG</Property>
				<Property Name="PKG_description" Type="Str"></Property>
				<Property Name="PKG_destinations.Count" Type="Int">1</Property>
				<Property Name="PKG_destinations[0].ID" Type="Str">{6C14BCA1-FD1E-4EEE-A8D9-A4F9C9189A78}</Property>
				<Property Name="PKG_destinations[0].Subdir.Directory" Type="Str">cRIO Replication Utility</Property>
				<Property Name="PKG_destinations[0].Subdir.Parent" Type="Str">root_5</Property>
				<Property Name="PKG_destinations[0].Type" Type="Str">Subdir</Property>
				<Property Name="PKG_displayName" Type="Str">cRIO Replication Utility</Property>
				<Property Name="PKG_displayVersion" Type="Str"></Property>
				<Property Name="PKG_feedDescription" Type="Str"></Property>
				<Property Name="PKG_feedName" Type="Str"></Property>
				<Property Name="PKG_homepage" Type="Str"></Property>
				<Property Name="PKG_hostname" Type="Str"></Property>
				<Property Name="PKG_maintainer" Type="Str">S2 Labs &lt;&gt;</Property>
				<Property Name="PKG_output" Type="Path">/C/zKirby/lv_PC Builds/NI_AB_PROJECTNAME/package</Property>
				<Property Name="PKG_packageName" Type="Str">crio-replication-utility</Property>
				<Property Name="PKG_publishToSystemLink" Type="Bool">false</Property>
				<Property Name="PKG_section" Type="Str">Application Software</Property>
				<Property Name="PKG_shortcuts.Count" Type="Int">1</Property>
				<Property Name="PKG_shortcuts[0].Destination" Type="Str">root_8</Property>
				<Property Name="PKG_shortcuts[0].Name" Type="Str">cRIO Replication Utility</Property>
				<Property Name="PKG_shortcuts[0].Path" Type="Path">cRIO Replication Utility</Property>
				<Property Name="PKG_shortcuts[0].Target.Child" Type="Str">{BCC7A01B-FDA9-4510-A8BD-25D12CC3A478}</Property>
				<Property Name="PKG_shortcuts[0].Target.Destination" Type="Str">{6C14BCA1-FD1E-4EEE-A8D9-A4F9C9189A78}</Property>
				<Property Name="PKG_shortcuts[0].Target.Source" Type="Ref">/My Computer/Build Specifications/cRIO Replication Utility</Property>
				<Property Name="PKG_shortcuts[0].Type" Type="Str">NIPKG</Property>
				<Property Name="PKG_sources.Count" Type="Int">1</Property>
				<Property Name="PKG_sources[0].Destination" Type="Str">{6C14BCA1-FD1E-4EEE-A8D9-A4F9C9189A78}</Property>
				<Property Name="PKG_sources[0].ID" Type="Ref">/My Computer/Build Specifications/cRIO Replication Utility</Property>
				<Property Name="PKG_sources[0].Type" Type="Str">EXE Build</Property>
				<Property Name="PKG_synopsis" Type="Str">cRIO_Replication_Utility</Property>
				<Property Name="PKG_version" Type="Str">1.0.2</Property>
			</Item>
		</Item>
	</Item>
</Project>
