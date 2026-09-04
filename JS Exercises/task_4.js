class University {
  constructor(name) {
    this.name = name;
    this.departments = [];
  }

  addDepartment(department) {
    this.departments.push(department);
  }

  removeDepartment(department) {
    this.departments = this.departments.filter((dept) => dept !== department);
  }

  displayDepartments() {
    console.log(`Departments at ${this.name}:`);
    this.departments.forEach((dept) => console.log(dept));
  }
}

const uni = new University("Oxford University");
uni.addDepartment("Computer Science");
uni.addDepartment("Mathematics");
uni.addDepartment("Physics");
uni.displayDepartments();

uni.removeDepartment("Physics");
uni.displayDepartments();
