export class LoginDTO {
    constructor(email, password) {
        this.email = email;
        this.password = password;
        this.timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    }
}
