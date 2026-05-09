def read_data(file_name):
    x_values = []
    y_values = []
    z_values = []
    time = []

    try:
        with open(file_name, 'r') as file:
            next(file)
            
            for line in file:
                parts = line.strip().split(',')
                
                x_values.append(float(parts[0]))
                y_values.append(float(parts[1]))
                z_values.append(float(parts[2]))
                time.append(float(parts[3]))
                
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

    return x_values, y_values, z_values, time
