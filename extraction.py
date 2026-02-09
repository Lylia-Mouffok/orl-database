function extraction()
% Extraction des vecteurs caractéristiques basés sur la wavelet coiflet


ORL_img_path = 'ORL database/s%d/%d.pgm';

% Création des dossiers train et test si inexistants
chemin_train = 'Train/';
chemin_test  = 'Test/';

if ~exist(chemin_train, 'dir'), mkdir(chemin_train); end
if ~exist(chemin_test, 'dir'), mkdir(chemin_test); end

% Initialisation des matrices
train_mat = [];
test_mat = [];

fprintf('Début de l''extraction des caractéristiques...\n');

for person_id = 1:40
    fprintf('Traitement de la personne %d/40...\n', person_id);
    
    for image_id = 1:10
        
        img_file_name = sprintf(ORL_img_path, person_id, image_id);
        
        if ~exist(img_file_name,'file')
            warning('Image manquante : %s', img_file_name);
            continue;
        end
        
        I = imread(img_file_name);

        % Décomposition wavelet Coiflet niveau 3
        [c, s] = wavedec2(double(I), 3, 'coif1');
        dims = s(1, :);
        Dimx = dims(1);
        Dimy = dims(2);
        v = c(1 : Dimx*Dimy);
        v = v(:); % vecteur colonne

        % Enregistrement individuel dans Train ou Test
        if image_id <= 5
            % 5 premières images -> Train
            train_mat = [train_mat v];
            nom_fichier = sprintf('%s%d_%d.fp', chemin_train, person_id, image_id);
            save(nom_fichier, 'v');
        else
            % 5 dernières images -> Test
            test_mat = [test_mat v];
            nom_fichier = sprintf('%s%d_%d.fp', chemin_test, person_id, image_id);
            save(nom_fichier, 'v');
        end
    end
end

% Sauvegarde des matrices complètes 
save('Mattrain.mat', 'train_mat');
save('Mattest.mat', 'test_mat');

fprintf('\nExtraction terminée \n');
fprintf('Taille train_mat : [%d x %d]\n', size(train_mat, 1), size(train_mat, 2));
fprintf('Taille test_mat : [%d x %d]\n', size(test_mat, 1), size(test_mat, 2));
fprintf('Nombre de vecteurs Train : %d\n', size(train_mat, 2));
fprintf('Nombre de vecteurs Test : %d\n', size(test_mat, 2));

end
