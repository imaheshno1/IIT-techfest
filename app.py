from flask import Flask, request, send_file
import pandas as pd
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded CSV files
        group_csv = request.files['group_csv']
        hostel_csv = request.files['hostel_csv']

        # Read CSV files into DataFrames
        group_df = pd.read_csv(group_csv)
        hostel_df = pd.read_csv(hostel_csv)

        # Allocate rooms
        allocation_df = allocate_rooms(group_df, hostel_df)

        # Create output CSV file
        output_csv = allocation_df.to_csv(index=False)

        # Return output CSV file as a downloadable file
        return send_file(StringIO(output_csv), as_attachment=True, attachment_filename='room_allocation.csv')

    return '''
        <h1>Room Allocation System</h1>
        <form action="" method="post" enctype="multipart/form-data">
            <input type="file" name="group_csv" required>
            <br>
            <input type="file" name="hostel_csv" required>
            <br>
            <input type="submit" value="Allocate Rooms">
        </form>
    '''

def allocate_rooms(group_df, hostel_df):
    # Create a dictionary to store the allocation
    allocation = {}

    # Iterate over each group
    for index, group in group_df.iterrows():
        group_id = group['Group ID']
        members = group['Members']
        gender = group['Gender']

        # Find a suitable hostel room
        hostel_room = find_hostel_room(hostel_df, gender, members)

        # If a suitable room is found, allocate the group
        if hostel_room is not None:
            allocation[group_id] = {
                'Hostel Name': hostel_room['Hostel Name'],
                'Room Number': hostel_room['Room Number'],
                'Members Allocated': members
            }

    # Create a DataFrame from the allocation dictionary
    allocation_df = pd.DataFrame.from_dict(allocation, orient='index')

    return allocation_df

def find_hostel_room(hostel_df, gender, members):
    # Filter hostel rooms by gender and capacity
    filtered_hostel_df = hostel_df[(hostel_df['Gender'] == gender) & (hostel_df['Capacity'] >= members)]

    # Sort filtered hostel rooms by capacity in ascending order
    filtered_hostel_df = filtered_hostel_df.sort_values(by='Capacity')

    # Return the first suitable hostel room
    for index, hostel_room in filtered_hostel_df.iterrows():
        return hostel_room

    # If no suitable room is found, return None
    return None

if __name__ == '__main__':
    app.run(debug=True)