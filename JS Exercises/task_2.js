function sumOfString(str) {
    return str
        .split(",")
        .reduce((sum, num) => sum + parseFloat(num.trim()), 0);
}

console.log(sumOfString("1.5, 2.3, 3.1, 4, 5.5, 6, 7, 8, 9, 10.9"));
