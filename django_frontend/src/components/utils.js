function getTimeStamp() {

    const timestamp = new Date().toLocaleTimeString("en-us", {
        hour: "2-digit",
        minute: '2-digit',
        hour12: false
    })
    return timestamp
}

function toDateTimeString(time) {
    return new Date(new Date().toLocaleDateString() + ' ' + '17:52').toISOString()
}
export { getTimeStamp, toDateTimeString };