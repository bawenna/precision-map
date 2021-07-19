import json
import statistics


def get_precision(mean, average_room_temp):
    pre = average_room_temp - mean
    if pre < 0:
        pre = -1 * pre
    return pre


def extension_validation(filename, ext: list = ["json"]) -> bool:
    """
    Validated the extension of files
    :param filename:
    :param ext: default json
    :return: bool
    """
    files_split = filename.split(".")
    ext_for_file = files_split[-1]
    if ext_for_file in ext:
        return True
    return False


def process_data_for_output(inputdata):
    try:
        formatted_data_objects = json.loads(inputdata.read())
        reference = formatted_data_objects.get("reference")
        information = formatted_data_objects.get("data")
        ref_humidity_reading = reference.get("ref-hum")
        ref_temp_reading = reference.get("ref-temp")
        final_data = dict()
        for name, objects in information.items():
            for type, value in objects.items():
                if type == 'thermometer':
                    # extract all the temperature data for calculation
                    temp_data = [x['data'] for x in value]
                    reading = statistics.mean(temp_data)
                    # required at least two datapoints
                    stdev = statistics.stdev(temp_data)
                    precision = get_precision(reading, ref_temp_reading)
                    if precision <= 0.5 and stdev < 3:
                        final_data[f"{name}_{type}"] = "ultra-precise"
                    elif precision <= 0.5 and stdev < 5:
                        final_data[f"{name}_{type}"] = "very precise"
                    else:
                        final_data[f"{name}_{type}"] = "precise"
                elif type == 'humidity':
                    # init an array to store each percentage for later
                    percentage_diff_array = []
                    for x in value:
                        diff = ref_humidity_reading - x['data'] if ref_humidity_reading - x['data'] > 0 else x['data'] - ref_humidity_reading
                        percentage_diff = ((diff / ref_humidity_reading) * 100)
                        percentage_diff_array.append(percentage_diff)
                    percentage_diff_mean = statistics.mean(percentage_diff_array)
                    if percentage_diff_mean > 1:
                        final_data[f"{name}_{type}"] = "discard"
                    else:
                        final_data[f"{name}_{type}"] = "keep"
                else:
                    final_data[f"{name}_{type}"] = "Unable to identify"
        return final_data, None
    except Exception as e:
        return None, e
