close all 
clear all
clc

b = 73e-3;
h = 1.65e-3;
L = 240e-3;

J = b*h^3/12;

E = 2.7e9; %Notre module: 2.7e9
dens = 1937.18;
mu = dens*b*h;

B = 3.6; %Amortissement


dt = 6e-5;

nx = 20; %Nombre d'éléments spaciaux
nt = 9000;

dx = L/(nx-1); %Pour la résolution du graph?
x = -dx:dx:L+dx; %Matrice d'éléments spaciaux
nx = nx + 2; %Nombre d'élément (+2 pour ajuster avec le dx de droit pis de gauche)

dx_n = dx; % Normalise that shit %ATTENTION NOUS AVONS PAS NORMALISÉ

kappa = sqrt(E*J/(mu*L^4)); %Chunk

mu_simu = kappa*dt/dx_n^2;



% if(mu_simu > 0.5)
%     warning("La simulation ne sera pas stable")
% end

% f1 = 1.875^2*kappa/(2*pi); %Dans un ti-power-point slides 34


%Conditions initales
F = zeros(1, nx); %Force
F(10) = -1;
temps = 0;
w = 1 * fliplr(0.001*sin(pi*x/(2*L))-0.001);
w_old = w; %Un pas dans le passé
w_new = zeros(1, nx);
w_init = w; %Préservation de la condition initiale

masse_bout = zeros(1, nt+1); %Vecteur qui contient la position de l'extrémité de la lame en fonction du temps

%Param pour speedy gonzalez 
% coeff1 = (2 - 6*mu_simu^2);
% coeff2 = (4*mu_simu^2);
% coeff3 = -mu_simu^2;

coeff1 = (E * J)/(dx_n^4);
coeff2 = mu/(dt^2);
coeff3 = B/dt;
coeff4 = ((mu/dt^2)+(B/dt))^(-1);

%Let's plot the figure
h = plot(x, 1000*w_init, x, 1000*w_new);
xlabel("X [m]")
ylabel("Déflexion [mm]")
ylim([-1.2,1.2])
grid on

for n=0:nt
    
    w_new = zeros(1, nx);
    i = 3:nx-2;
    %w_new(i) = coeff1*w(i) + coeff2*(w(i+1)+w(i-1))+coeff3*(w(i+2)+w(i-2))-w_old(i);  %La grande ligne
    w_new(i) = (-coeff1*(w(i+2)-4*w(i+1)+6*w(i)-4*w(i-1)+w(i-2)) - coeff2*(-2*w(i)+w_old(i)) + coeff3*w(i) + F(i)/dx_n)*coeff4; %La grosse ligne
    
    %condi limit
    w_new(1:2) = 0;
    w_new(end-1) = 2*w_new(end-2)-w_new(end-3);
    w_new(end) =2*w_new(end-1)-w_new(end-2);
    
    %Prep next turn
    w_old = w;
    w = w_new;
    
    masse_bout(n+1) = w(end);
    
    set(h(2), "Ydata", 1000*w_new);
    drawnow
end
figure 
plot((0:dt:(nt*dt)), masse_bout)
grid
