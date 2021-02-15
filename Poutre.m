% %Posons les constantes nécessaires
% longueur = 0.3;
% largeur = 0.05;
% epaisseur = 0.001;
% Young = 2.7*10^11;
% load = -2;
% poid = -0.1;
% 
% I = (1/12) * epaisseur^3 * largeur;
% a = longueur/2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Section est le code a charlé
% x = linspace(0, 1, 100);
% y = linspace(0, 1, 100); 
% %Boucle générant le graph
% for count=1:length(y)
%     y(count) = count*count*(1.5*count)/3000000; %J'ai uncune caliss d'idée de l'utilité de cette fonction
% end
% for count=0:200 %Nombre d'itération
%     plot(x, y-y*cos(count/10)*exp(-count/100))
%     axis([0 1 -1 1])
%     pause(0.1) %Pause de 0.01 par frame
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Fin du code à charlé

n = 50;
XY = 10 * rand(2,n) - 5;
for i=1:n
    plot(XY(1,i),XY(2,i), "or")
    axis([-20 20 -20 20])
    pause(.1)
end


%%HELLO TRUC DE PRO! SI TU SOUHAITES METTRE UN BLOC EN COMMENTAIRE,
%%SÉLECTIONNE LE PIS CLIQUE-DROIT ET CLIQUE SUR COMMENT OU SUR UNCOMMENT
















