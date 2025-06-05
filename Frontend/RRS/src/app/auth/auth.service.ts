import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _isAuthenticated = false;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {} // Inyecta PLATFORM_ID

  private safeLocalStorage(): Storage | null {
    return isPlatformBrowser(this.platformId) ? localStorage : null;
  }

  login(email: string, password: string): boolean {
    if (email === 'admin@empresa.com' && password === '123456') {
      this._isAuthenticated = true;
      this.safeLocalStorage()?.setItem('auth', 'true'); // Uso seguro
      return true;
    }
    return false;
  }

  logout(): void {
    this._isAuthenticated = false;
    this.safeLocalStorage()?.removeItem('auth'); // Uso seguro
  }

  isAuthenticated(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return this._isAuthenticated || this.safeLocalStorage()?.getItem('auth') === 'true';
    }
    return this._isAuthenticated; // Fallback para SSR
  }
}