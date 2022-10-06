function MRAWpreview(it, folder_mraw)
%%
% addpath 'C:\Users\user\Desktop\Zárate\LFD_MPIV_toolbox';
%%
fileName = 'videito.mraw';
load(fullfile(folder_mraw, sprintf('videito.mat')));
mrawParam;
% DATA=data_PIV
[ImDat]=readmraw_cz(folder_mraw,fileName,0,mrawParam);
maxvalue=max(max(max(ImDat.Images.RawImages)));
minvalue=mean(min(min(ImDat.Images.RawImages)));

%% Preview
figure(2)
hist=histogram(ImDat.Images.RawImages(:),2^16);

% Mean Background
MeanValue=mean(ImDat.Images.RawImages,3);
B=repmat(MeanValue,[1 1 size(ImDat.Images.RawImages,3)]);
B=uint16(B);
maxvalue=max(max(max(ImDat.Images.RawImages)));
ImDat.Images.RawNoBackground=ImDat.Images.RawImages-(B);%-(H);
figure(3)
set(gcf, 'Position', [360.2000 34.6000 839.2000 748]);
for j=1:mrawParam.TotalFrames
%     imshow(remove_background(ImDat.Images.RawImages(:,:,j),'avg'),'InitialMagnification','fit');
    subplot(2,1,1)
    imshow(imadjust(ImDat.Images.RawNoBackground(1:end-10,1:end,j)),'InitialMagnification',150)
    title('Avg Filter')
    subplot(2,1,2)
    imshow(imadjust(ImDat.Images.RawImages(1:end-10,1:end,j)),'InitialMagnification',150)
    title('Original')
    axis tight
    drawnow()
    pause(0.008)
end
end

function [ImageData] = readmraw_cz(folder_mraw, filename,numimgs,handles)
%   readmraw.m 
%   READMRAW Read 16 bit monchrome Photron image data into a structure
%   
%   I=READMRAW('c:\Photron\Filename',[a,b]) loads images a through b from
%   'c:\Photron\Filename' into structure I.  
%
%   Remarks
%   -------
%   This function must be handed the common *.cih and *.mraw file name 
%   and the range of images to be loaded (Matlab can not handle the entire
%   image range for large files).  A file extension is not allowed.
%   This function is intended for monochrome 16 bit *.mraw files only.
%   NOTE: Both the *.cih file and the *.mraw file are utilized
%   Autor: SEP                                Creation Date: June 20,2013
%
%   Examples
%   --------
%   % Load all images
%   I=readmraw('c:\Photron\Moviefile',[0]); 
%   % Load images 10 through 50
%   I=readmraw('c:\Photron\Moviefile',[10,50]);
%   % Load image 10
%   I=readmraw('c:\Photron\Moviefile',[10]);

fid2=fopen(fullfile(folder_mraw,filename),'r');
if fid2<1 display([filename ' filenames could not be found']); ImageData=0; return; end

% Read Header Information
% Header=textscan(fid1,'%s','delimiter',':');
Total_Frames=handles.TotalFrames;
Width=handles.Width;
Height=handles.Height;
CameraSetup.FrameRate=handles.FrameRate;
%Other data from header if desired
Pixels=Width*Height;

% Define Image Range
if numimgs==0               % load all the images 
    first_frame=1;
    frames=Total_Frames;
elseif (length(numimgs)==1) % load a single image
    first_frame=numimgs;
    frames=1;
else                        % load a specified range of images
    first_frame=numimgs(1,1);
    last_frame=numimgs(1,2);
    frames=last_frame-first_frame+1;
end

%Load Images
fseek(fid2,(first_frame-1)*Pixels*2,'bof');
I=zeros(Pixels,frames,'uint16');
for n=1:1:frames
    I(:,n)=(fread(fid2,Pixels,'uint16'));
end
fclose(fid2);
N = [Width Height frames];
ImageData.Images.RawImages=permute(reshape(I,N),[2 1 3]);
ImageData.CameraSetup=CameraSetup;
end
