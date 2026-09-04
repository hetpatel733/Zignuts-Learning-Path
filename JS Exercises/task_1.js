function sumNumbersInString(str) {
    const numbers = str.match(/\d+/g);
    if (!numbers) return 0;
    return numbers.reduce((sum, num) => sum + Number(num), 0);
}

console.log(sumNumbersInString("foo8bar8cat2tc2"));
