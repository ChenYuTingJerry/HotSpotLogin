import httplib2
import json
from subprocess import check_output


def adjust_mac_format(mac):
    result = []
    for code in mac.split(':'):
        if len(code) == 1:
            result.append('0'+code.upper())
        else:
            result.append(code.upper())

    return ':'.join(result)


def get_current_info():
    output = check_output(['airport', '-I'])
    if output.find('Off') == -1:
        infos = output.split('\n')
        currentAp = dict()
        for info in infos[:-1]:
            key, value = info.lstrip().split(': ')
            if key == 'BSSID':
                currentAp['macAddress'] = adjust_mac_format(value)
            elif key == 'agrCtlRSSI':
                currentAp['signalStrength'] = value
            elif key == 'agrCtlNoise':
                currentAp['noise'] = value
            elif key == 'channel':
                currentAp['channel'] = value
        currentAp['signalToNoiseRatio'] = str(int(currentAp['signalStrength']) - int(currentAp['noise']))
        return currentAp


def get_ap_info():
    current_ap = get_current_info()
    print current_ap
    output = check_output(['airport', '-s'])
    results = output.split('\n')
    ap_info_list = list()
    for result in results[1:-1]:
        ap_info = dict()
        infoList = result.split()
        ap_info['channel'] = infoList[-4]
        ap_info['signalStrength'] = infoList[-5]
        ap_info['macAddress'] = infoList[-6].upper()
        if ap_info['macAddress'] == current_ap.get('macAddress'):
            ap_info['signalToNoiseRatio'] = current_ap['signalToNoiseRatio']
        print ' '.join(infoList[:len(infoList)-6]) + ': '+ ap_info['macAddress']
        # ap_info['name'] = ' '.join(infoList[:len(infoList)-6])
        ap_info_list.append(ap_info)

    return ap_info_list


def main():
    h = httplib2.Http()
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAFziExyA44NkrNcuQhbFovec8_vc8ouTA'
    ap_list = get_ap_info()
    post_data = {'wifiAccessPoints': ap_list}
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    print json.dumps(post_data)
    resp, content = h.request(url, method='POST', body=json.dumps(post_data), headers=headers)
    print content


if __name__ == "__main__":
    main()
