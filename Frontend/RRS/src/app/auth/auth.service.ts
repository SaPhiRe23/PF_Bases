import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _isAuthenticated = false;

  login(email: string, password: string): boolean {
    if (email === 'admin@empresa.com' && password === '123456') {
      this._isAuthenticated = true;
      localStorage.setItem('auth', 'true');
      return true;
    }
    return false;
  }

  logout() {
    this._isAuthenticated = false;
    localStorage.removeItem('auth');
  }

  isAuthenticated(): boolean {
    return this._isAuthenticated || localStorage.getItem('auth') === 'true';
  }
}

