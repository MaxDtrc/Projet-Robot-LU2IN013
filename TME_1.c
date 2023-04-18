#include "TME.h"

//Excercice 1
//Q 1.3
int hashFile(char* source, char* dest){
    char commande[100];
    sprintf(commande, "cat %s | sha256sum > %s",source,dest);//Pour linux
    //sprintf(commande, "shasum -a 256 %s > %s",source,dest);//Pour macOs
    system(commande);
    return 0; 
}

//Q 1.4
char* sha256file(char *file) {

    /* renvoie le hash du fichier donné */

    static char template[] = "/tmp/myfileXXXXXX";
    char fname[18];
    strcpy(fname, template);
    int fd = mkstemp(fname);
    if (fd == -1) {
		printf("Erreur création fichier temporaire \n");
		exit(1);
	}
    
	hashFile(file, fname);

    FILE *f = fopen(fname, "r");
	char* hash = (char*)malloc(sizeof(char)*256);
	fread(hash, 256, 1, f);
	fclose(f);
	unlink(template);
    
    char rm[10000];
    sprintf( rm , "rm %s" , fname ) ;
    system(rm) ;
    hash[64] = '\0';
    return hash ;

}

//Exercice 2



//Q 2.1
List* initList(){
    List* l = malloc(sizeof(List));
    return l;
}

//Q 2.2
Cell* buildCell(char* ch){
    Cell* c = (Cell*)malloc(sizeof(Cell));
    c->data=strdup(ch);
    c->next=NULL;
    return c;
}

//Q 2.3
void insertFirst(List* l, Cell* c){
    c->next=*l;
    *l=c;
}

//Q 2.4
char* ctos(Cell* c){
    if(c!=NULL){
        return c->data;
    }
    return NULL;
}


char* ltos(List* l){
    Cell* c= *l;
    char *s=malloc(sizeof(char)*256);
    while(c){
        strcat(s, ctos(c));
        strcat(s ,"|");
        c=c->next;
    }
    return s;
}

//Q 2.5
Cell* listGet(List* l, int i){
    Cell* c= l[0];
    int cpt=0;
    while(cpt<i && c!=NULL){
        cpt++;
        c= c->next;
    }
    return c;
}

//Q 2.6
Cell* searchList(List* l, char* str){
    Cell* c= *l;
    while(c!=NULL){
        if(strcmp(ctos(c),str)!=0)
            c= c->next;
        else
            return c;
    }
    return c;
}

//Q 2.7
List* stol(char* s){
    int pos=0;
    int n_pos=0;
    int sep='|';
    char *ptr ;
    char *result=malloc(sizeof(char)*1000);
    List *L=initList();
    while (pos<strlen(s)){
        ptr=strchr(s+pos, sep);
        if(ptr==NULL)
            n_pos=strlen(s)+1;
        else{
            n_pos=ptr-s+1;
        }
        memcpy(result, s+pos, n_pos-pos-1);
        result[n_pos-pos-1]='\0';
        pos=n_pos;
        insertFirst(L, buildCell(result));
        result[0]='\0';
    }
    return L;
}


//Q 2.8
void ltof(List* l, char* path){
    FILE* f= fopen(path,"w");
    char* lst=ltos(l);
    fputs(lst,f);
    fclose(f);
}
List* ftol(char* path){
    FILE* f=fopen(path,"r");
    char* str=malloc(sizeof(char)*256);
    str[0] = '\0';
    fgets(str,256*sizeof(char),f);
    fclose(f);
    return stol(str);
}


//Exercice 3
//Q 3.1
List* listdir(char* root_dir){
    List* res=initList();
    Cell* tmp;
    DIR* dp=opendir(root_dir);
    struct dirent *ep;
    if (dp != NULL){
        while ((ep=readdir(dp))!=NULL){
            //printf("_%s \n", ep->d_name);
            tmp=buildCell(ep->d_name);
            insertFirst(res, tmp);
        }
    }
    tmp=NULL;
    return res;
}

//Q 3.2
void freeList(List* lst){
    Cell* c=*lst;
    Cell* tmp=NULL;

    while(c!=NULL){
        tmp=c->next;
        free(c->data);
        free(c);
        c=tmp;
    }
    free(lst);
}

struct stat st = {0};

int file_exists(char *file){
    struct stat buffer;
    return (stat(file, &buffer) == 0);
}

//Q 3.3
void cp(char *to, char *from){
    if(file_exists(from)==0){
        printf("(cp) le fichier source n'existe pas\n");
    }
    else{
        FILE *src=fopen(from,"r");
        FILE *dest=fopen(to,"w");
        char c[256];
        while (fgets(c, 256, src)!=NULL){
            fputs(c,dest);
        }

        fclose(src);
        fclose(dest);
    }
}
//Q 3.4
char* hashToPath(char* hash) {

	/* Retourne le chemin d'un fichier a partir de son hash */

	char* path = (char*) malloc((strlen(hash)+1)*sizeof(char));
	if (path == NULL) {
		printf("Erreur allocation mémoire\n");
		exit(1);
	}
	
	strncpy(path, hash, 2);
	path[2] = '/';
	strcpy(path + 3, hash + 2);

	return path;

}


//mkdir ??
//Q 3.5
void blobFile(char* file){
    //creation d'un nom de fichier aléatoire
    static char template[] = "myfileXXXXXX";
    char fname[100];
    strcpy(fname, template);
    mkstemp(fname);

    //création du fichier
    char* commande=malloc(sizeof(char)*100);
    sprintf(commande,"cp -R %s %s",file,fname);
    system(commande);
    
    //copie
    cp(file, fname);
    printf("copie de %s à %s\n",file, fname);
}