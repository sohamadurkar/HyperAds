# Function to get the public IP address of your system
function Get-IpAddress {
    $ip = (Invoke-RestMethod -Uri "http://ipinfo.io/json").ip
    return $ip
}

# Function to get latitude and longitude using the IP address
function Get-Location {
    $ip = Get-IpAddress
    $url = "https://ipinfo.io/$ip/loc"
    $location = Invoke-RestMethod -Uri $url
    $coords = $location -split ","
    return @{ Latitude = $coords[0]; Longitude = $coords[1] }
}

# Function to send location data to Flask server
function Send-Location {
    param (
        [string]$latitude,
        [string]$longitude
    )

    $url = "http://10.188.154.159:5000/update-location"  # Replace <your-laptop-ip> with your actual laptop IP
    $headers = @{
        "Content-Type" = "application/json"
    }

    # Construct the JSON payload with latitude and longitude
    $body = @{
        latitude = $latitude
        longitude = $longitude
    } | ConvertTo-Json

    # Send the location to Flask server
    Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
}

# Infinite loop to send location periodically (every 10 seconds)
while ($true) {
    $location = Get-Location
    if ($location) {
        $latitude = $location.Latitude
        $longitude = $location.Longitude
        Write-Host "Sending Location: Latitude = $latitude, Longitude = $longitude"
        Send-Location -latitude $latitude -longitude $longitude
    } else {
        Write-Host "Unable to fetch GPS location."
    }

    # Wait for 10 seconds before sending again
    Start-Sleep -Seconds 10
}
