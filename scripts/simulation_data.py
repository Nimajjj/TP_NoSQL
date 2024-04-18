import json
from faker import Faker

class UserSimulator:
    def __init__(self, total_users=100):
        self.fake = Faker()
        self.total_users = total_users
        self.user_data = []

    def generate_user_info(self):
        user_profile = {
            "name": self.fake.name(),
            "age": self.fake.random_int(min=1, max=90),
            "email": self.fake.email(),
            "joined": self.fake.date_time_this_decade().isoformat()
        }
        return user_profile

    def create_users(self):
        for _ in range(self.total_users):
            user_info = self.generate_user_info()
            self.user_data.append(user_info)

    def save_to_json(self, file_path):
        with open(file_path, "w") as json_file:
            json.dump(self.user_data, json_file, indent=2)

# Executing user simulation
if __name__ == "__main__":
    user_simulator = UserSimulator()
    user_simulator.create_users()
    user_simulator.save_to_json("./data/generated_users.json")

