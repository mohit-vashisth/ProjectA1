export class Signup {
    constructor(userName, userEmail, contactNumber, userPassword, privacyCheck) {
        this.userName = userName;
        this.userEmail = userEmail;
        this.contactNumber = contactNumber;
        this.userPassword = userPassword;
        this.timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        this.privacyCheck = privacyCheck;
    }
}
