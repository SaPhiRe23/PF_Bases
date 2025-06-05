import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private API_URL = 'http://localhost:8000';
  private authState = new BehaviorSubject<boolean>(!!localStorage.getItem('token'));
  isAuthenticated$ = this.authState.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  storeSession(token: string, role: string) {
    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
    this.authState.next(true);
  }

  logout() {
    localStorage.clear();
    this.authState.next(false);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  // Usuarios
  crearUsuario(data: any) {
    return this.http.post(`${this.API_URL}/usuarios/`, data);
  }

  obtenerUsuarios(params?: any) {
    return this.http.get(`${this.API_URL}/usuarios/`, { params });
  }

  // Citas
  crearCita(data: any) {
    return this.http.post(`${this.API_URL}/citas/`, data);
  }

  login(email: string, password: string) {
    return this.http.post(`${this.API_URL}/login`, { email, password });
  }

  getUserRole(): string | null {
    return localStorage.getItem('role');
  }

}