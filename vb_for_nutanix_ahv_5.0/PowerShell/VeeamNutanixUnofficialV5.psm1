

function Get-NutanixVeeamAuthJwtToken {
    $thumbprint = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Veeam\AHV").Thumbprint
    $VeeamAuthPath = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Veeam\Veeam Backup and Replication\Plugins\12.0.0\Console\AHV").InstallationPath.replace('Console', 'Service') + "VeeamAuth.exe"

    $result = &"$VeeamAuthPath" "/purpose:DATA" "/clientCertificateThumbprint:$thumbprint" "/platformId:{799A5A3E-AE1E-4EAF-86EB-8A9ACC2670E2}"
    $token = ($result -match "JWT=.*").Substring(4).Replace('\r\n','')

    return $token
}

function Get-NutanixPlatformServiceToken {
    $uri = "https://localhost:8543/api/v2/account/login"
    $body = @{
        "token" = Get-NutanixVeeamAuthJwtToken
    } | ConvertTo-Json
    $req = Invoke-WebRequest -Uri $uri `
    -Method "POST" `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing
    return ($req.Content | ConvertFrom-Json).token
}

function Get-NutanixVmMetadata($restorePointUuid){
    $uri = "https://localhost:8543/api/v2/vmRestorePoints/$restorePointUuid/retrieveMetadata"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "POST" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json).virtualMachineMetadata
}

function Get-VbrVmMetadata($restorePointUuid){
    $uri = "https://localhost:6172/api/vmRestorePoints/$restorePointUuid/metadata"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = "Bearer $(Get-NutanixVeeamAuthJwtToken)";
        "x-api-version" = "1.0-rev41"
    }
    return ($req.Content | ConvertFrom-Json)
}


function Publish-NutanixVm($clusterUuid, $containerUuid, $networkUuid, $namePrefix, $restorePointUuid, $restoreReason){
    $vmMeta = Get-NutanixVmMetadata -restorePointUuid $restorePointUuid
    $vmMetaDetailed = Get-VbrVmMetadata -restorePointUuid $restorePointUuid

    $disksSpec = New-Object System.Collections.Generic.List[System.Object]
    $containerName = (Get-NutanixClusterStorageContainer -clusterUuid $clusterUuid -containerUuid $containerUuid).name
    foreach($disk in ($vmMetaDetailed.disks).members){
        $diskSpec = @{
            "diskId" = $disk.diskId;
            "diskKey" = $disk.diskKey;
            "storageContainerId" = $containerUuid;
            "storageContainerName" = $containerName;
        }
        $disksSpec.Add($diskSpec)
    }
    
    $networkAdaptersSpec = New-Object System.Collections.Generic.List[System.Object]
    $networName = (Get-NutanixClusterNetwork -clusterUuid $clusterUuid -networkUuid $networkUuid).name
    foreach($adapter in $vmMeta.networks){
        $networkAdapterSpec = @{
            "networkId" = $networkUuid;
            "networkName" = $networName;
            "adapterMac" = $adapter.adapterMac;
        }
        $networkAdaptersSpec.Add($networkAdapterSpec)
    }

    $uri = "https://localhost:8543/api/v2/irsessions"
    $body = @{
        "clusterId" = $clusterUuid;
        "forceDeleteExistingVm" = $false;
        "disks" = $disksSpec;
        "networks" = $networkAdaptersSpec ;
        "oldVirtualMachineName" = $vmMeta.virtualMachineName;
        "newVirtualMachineName" = $namePrefix + $vmMeta.virtualMachineName;
        "powerOnVmAfterRestore" = $true;
	    "preserveOriginalVmUid" = $false; # IMPORTANT TO AVOID ORIGINAL VM OVERRIDE
	    "vmRestorePointId" = $restorePointUuid;
	    "disconnectNetworksAfterRestore" = $false;
        "reason" = $restoreReason
    } | ConvertTo-Json
    $req = Invoke-WebRequest -Uri $uri `
    -Method "POST" `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}

function Unpublish-NutanixVm($sessionTag){
    $uri = "https://localhost:8543/api/v2/irsessions/$sessionTag/stop"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "POST" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}

function Get-NutanixClusters(){
    $uri = "https://localhost:8543/api/v2/clusters"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json).members
}

function Get-NutanixClusterNetworks($clusterUuid){
    $uri = "https://localhost:8543/api/v2/clusters/$clusterUuid/networks"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json).members
}

function Get-NutanixClusterNetwork($clusterUuid, $networkUuid){
    $uri = "https://localhost:8543/api/v2/clusters/$clusterUuid/networks/$networkUuid"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}

function Get-NutanixClusterStorageContainers($clusterUuid){
    $uri = "https://localhost:8543/api/v2/clusters/$clusterUuid/storageContainers"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json).members
}

function Get-NutanixClusterStorageContainer($clusterUuid, $containerUuid){
    $uri = "https://localhost:8543/api/v2/clusters/$clusterUuid/storageContainers/$containerUuid"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}

function Get-VbrSessionByTag($sessionTag){
    $uri = "https://localhost:6172/api/restoreSessions/$sessionTag"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = "Bearer $(Get-NutanixVeeamAuthJwtToken)";
        "x-api-version" = "1.0-rev41"
    }
    return ($req.Content | ConvertFrom-Json)
}


function Get-NutanixIrSession($sessionTag){
    $uri = "https://localhost:8543/api/v2/irsessions/$sessionTag"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}

function WaitForIrMount($irSessionTag){
    $MaxTimeoutSec = 5 * 60 # 5 minutes
    $TimeWaitedSec = 0
    $TimeoutBetweenRetriesSec = 5
    do{
        Start-Sleep -Seconds $TimeoutBetweenRetriesSec 
        $TimeWaitedSec += $TimeoutBetweenRetriesSec 
        #$session = Get-VbrSessionByTag -sessionTag $irSessionTag
        $session = Get-NutanixIrSession -sessionTag $irSessionTag
    } While ($session.state -ne 'Mounted' -and $TimeWaitedSec -lt $MaxTimeoutSec)
}

function Get-NutanixVM($clusterUuid, $vmUuid){
    $uri = "https://localhost:8543/api/v2/clusters/$clusterUuid/vms/$vmUuid"
    $req = Invoke-WebRequest -Uri $uri `
    -Method "GET" `
    -ContentType "application/json" `
    -UseBasicParsing `
    -Headers @{
        "authorization" = Get-NutanixPlatformServiceToken
    }
    return ($req.Content | ConvertFrom-Json)
}